import os
import sys
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from US_visa.entity.config_entity import DataIngestionConfig
from US_visa.logger import logging
from US_visa.exception import USvisaException
from US_visa.entity.artifact_entity import DataIngestionArtifact
from US_visa.data_access.usvisa_data import USvisaData


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise USvisaException(e, sys) 
        
    def export_data_into_feature_store(self) -> DataFrame:
        try:
            logging.info("Exporting data from mongodb")
            usvisa_data = USvisaData()
            dataframe = usvisa_data.export_collection_dataframe(collection_name=
                                                                self.data_ingestion_config.collection_name)

            logging.info(f'Shape of dataframe: {dataframe.shape}')
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)

            os.makedirs(dir_path,exist_ok=True)
            logging.info(f'Saving exported data into feature store file: {feature_store_file_path}')
            dataframe.to_csv(feature_store_file_path, index=False,header=True)
            return dataframe
        except Exception as e:
            raise USvisaException(e, sys)
        
    def split_data_as_training_and_testing(self, dataframe: DataFrame) -> None:
        logging.info('Entered split data as train test method of Data Ingestion class')
        try:
            (train_set), (test_set) = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info('Performed train test split on the dataframe')
            logging.info('Exited split data as train test method of Data Ingestion class')

            dir_path = os.path.dirname(self.data_ingestion_config.tranining_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.tranining_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info(f'Exported train and test file path')
        
        except Exception as e:
            raise USvisaException(e, sys)
        
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info('Entered initiate data ingestion method of Data Ingestion class')

        try:
            dataframe = self.export_data_into_feature_store()
            logging.info('Got the data from mongodb')

            self.split_data_as_training_and_testing(dataframe)
            logging.info('Performed train test split on the dataset')

            logging.info('Exited initiate data ingestion method of Data Ingestion class')
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.tranining_file_path,
                                                            test_file_path=self.data_ingestion_config.testing_file_path)
            
            logging.info(f'Data Ingestion artifact: {data_ingestion_artifact}')

            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e, sys)
        
        
