import sys
from US_visa.exception import USvisaException
from US_visa.logger import logging  
from US_visa.components.data_ingestion import DataIngestion
from US_visa.components.data_validation import DataValidation
from US_visa.entity.config_entity import DataIngestionConfig,DataValidationConfig
from US_visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
    
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
        
    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)

        except Exception as e:
            raise USvisaException(e,sys)
