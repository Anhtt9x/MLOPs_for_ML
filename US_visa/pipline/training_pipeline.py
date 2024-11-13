import sys
from US_visa.exception import USvisaException
from US_visa.logger import logging  
from US_visa.components.data_ingestion import DataIngestion
from US_visa.components.data_validation import DataValidation
from US_visa.components.data_transformation import DataTransformation
from US_visa.components.model_trainer import ModelTrainer
from US_visa.components.model_evaluation import ModelEvaluation
from US_visa.components.model_pusher import ModelPusher
from US_visa.entity.config_entity import (DataIngestionConfig,DataValidationConfig,
                                          DataTransformationConfig, ModelTrainerConfig,
                                          ModelEvaluationConfig,
                                          ModelPusherConfig)

from US_visa.entity.artifact_entity import (DataIngestionArtifact,DataValidationArtifact,
                                            DataTransformationArtifact,ModelEvaluationArtifact,
                                            ModelTrainerArtifact,ModelPusherArtifact)



class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info('Entered the start_data_ingestion method of TrainPipeline class')
            logging.info('Getting the data from mongodb')
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info('Got the train set and test set from the mongodb')
            logging.info('Exited the start data ingestion method of TrainPipeline class')

            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e,sys)
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidation:
        try:
            logging.info('Entered the start_data_validation method of TrainPipeline class')
            logging.info('Starting the data validation')
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config)
            
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info('Data validation completed')
            logging.info('Exited the start data validation method of TrainPipeline class')
            return data_validation_artifact
        
        except Exception as e:
            raise USvisaException(e,sys)
        
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact, data_ingestion_artifact:DataIngestionArtifact) -> DataTransformationArtifact:
        try:
            logging.info('Entered the start_data_transformation method of TrainPipeline class')
            logging.info('Starting the data transformation')
            data_transformation = DataTransformation(data_transformation_config=self.data_transformation_config,
                                                     data_validation_artifact=data_validation_artifact,
                                                     data_ingestion_artifact=data_ingestion_artifact)
            
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise USvisaException(e,sys)
    
    def start_model_trainer(self, data_transform_artifact:DataTransformationArtifact):
        try:
            logging.info('Entered the start_model_trainer method of TrainPipeline class')
            
            model_trainer = ModelTrainer(data_transformation_artifact=data_transform_artifact,
                                                  model_trainer_config=self.model_trainer_config)
            
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise USvisaException(e,sys)
        
    def start_model_evaluation(self, data_ingestion_artifact:DataIngestionArtifact,
                               model_trainer_artifact:ModelTrainerArtifact)->ModelEvaluationArtifact:
        try:
            model_evaluation = ModelEvaluation(model_eval_config=self.model_evaluation_config,
                                               data_ingestion_artifact=data_ingestion_artifact,
                                               model_trainer_artifact=model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise USvisaException(e,sys)
        

    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact)->ModelPusherArtifact:
        try:
            model_pusher = ModelPusher(model_pusher_config=self.model_pusher_config,
                                       model_evaluation_artifact=model_evaluation_artifact)
            
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except Exception as e:
            raise USvisaException(e,sys)

        
    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact, data_ingestion_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_ingestion_artifact,model_trainer_artifact)
            if not model_evaluation_artifact.is_model_accepted:
                logging.info("Model is not accepted")
                return None
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact)
        except Exception as e:
            raise USvisaException(e,sys)
