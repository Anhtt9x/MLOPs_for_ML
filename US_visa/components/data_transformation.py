import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer

from US_visa.constants import *
from US_visa.entity.config_entity import DataTransformationConfig
from US_visa.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact,DataValidationArtifact
from US_visa.exception import USvisaException
from US_visa.logger import logging
from US_visa.utils.main_utils import save_object, save_numpy_array_data,read_yaml_file,drop_columns
from US_visa.entity.estimator import TargetValueMapping


class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config:DataTransformationConfig,
                 data_validation_artifact:DataValidationArtifact):
        
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

        except Exception as e:
            raise USvisaException(e,sys)
        
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USvisaException(e,sys)
    
    def get_data_transformer_object(self) -> Pipeline:
        logging.info('Entered get data transformer object method of DataTransformation class')
        try:
            logging.info('Got numerical cols from schema config')
            numeric_transformer = StandardScaler()
            oh_transformer = OneHotEncoder()
            ordinal_transformer = OrdinalEncoder()

            logging.info('Initialized StandardScaler, OneHotEncoder and OrdinalEncoder')

            oh_columns = self._schema_config['oh_columns']
            ordinal_columns = self._schema_config['or_columns']
            transform_columns = self._schema_config['transform_columns']
            num_features = self._schema_config['num_features']

            logging.info('Initialize PowerTransformer')

            transform_pipe = Pipeline(steps=[
                ('transformer', PowerTransformer(method='yeo-johnson'))
            ])      

            preprocessor = ColumnTransformer(
                [
                    ('OneHotEncoder', oh_transformer, oh_columns),
                    ('OrdinalEncoder', ordinal_transformer, ordinal_columns),
                    ('Transformer', transform_pipe, transform_columns),
                    ('StandardScaler', numeric_transformer, num_features)
                ]
            )

            logging.info('Created preprocess object from columnTransformer')
            logging.info('Exited get data transformer object method of DataTransformation class')
            return preprocessor
        except Exception as e:
            raise USvisaException(e,sys)
        

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            if self.data_validation_artifact.validation_status:
                logging.info("Starting data transformation")
                preprocessor = self.get_data_transformer_object()
                logging.info('Got preprocessor object')

                train_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
                test_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)
                logging.info('Read train and test data')

                input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_train_df = train_df[TARGET_COLUMN]
                logging.info('Got train features and test features of Training dataset')

                input_feature_train_df['company_age'] = CURRENT_YEAR - input_feature_train_df['yr_of_estab']
                logging.info('Added company age column to train dataset')

                drop_cols = self._schema_config['drop_columns']
                logging.info('Drop the columns in drop cols of Training dataset')

                input_feature_train_df = drop_columns(df=input_feature_train_df, cols=drop_cols)

                target_feature_train_df = target_feature_train_df.replace(
                    TargetValueMapping()._asdict()
                )

                input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_test_df = test_df[TARGET_COLUMN]
                input_feature_test_df['company_age'] = CURRENT_YEAR - input_feature_test_df['yr_of_estab']

                logging.info('Added company age column to test dataset')

                input_feature_test_df = drop_columns(df=input_feature_test_df, cols=drop_cols)

                logging.info('Drop the columns in drop cols of Test dataset')

                target_feature_test_df = target_feature_test_df.replace(
                    TargetValueMapping()._asdict()
                )

                logging.info('Got train features and test features of Test dataset')
                logging.info('Applying preprocessing object on training dataframe and testing dataframe')

                input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)

                logging.info('Used the preprocessor object to fit transform the train features')

                input_feature_test_arr = preprocessor.transform(input_feature_test_df)

                logging.info('Used the preprocessor object to transform the test features')
                logging.info('Applying SMOTEENN on Training Dataset')
                smt = SMOTEENN(sampling_strategy='minority')

                input_feature_train_final , target_feature_train_final = smt.fit_resample(input_feature_train_arr,
                                                                                          target_feature_train_df)
                
                logging.info('Applied SMOTEENN on training dataset')
                logging.info('Applying SMOTEENN on testing Dataset')

                input_feature_test_final, target_feature_test_final = smt.fit_resample(input_feature_test_arr,
                                                                                       target_feature_test_df)
                
                logging.info('Appilied SMOTEENN on Testing dataset')
                logging.info('Created train array and test array')

                train_arr = np.c_[
                    input_feature_train_final,np.array(target_feature_train_final)
                ]

                test_arr = np.c_[
                    input_feature_test_final,np.array(target_feature_test_final)
                ]

                save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)

                logging.info('Save the preprocessor object')
                logging.info('Exited initiate data transformation method of Data Tranformation class')

                data_tranformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )

                return data_tranformation_artifact
            else:
                raise Exception(self.data_validation_artifact.message)    
        
        except Exception as e:
            raise USvisaException(e,sys)