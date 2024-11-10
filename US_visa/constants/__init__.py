import os
from datetime import date

DATABASE_NAME = "EasyVisa"
COLLECTION_NAME = "Visa"

MONGODB_URL_KEY = "mongodb+srv://anhtt454598:gaucho0123456@cluster0.4nn7i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


PIPELINE_NAME:str = 'usvisa'
ARTIFACTS_DIR:str = 'artifacts'
TRAIN_FILE_NAME:str = 'train.csv'
TEST_FILE_NAME:str = 'test.csv'
FILE_NAME:str = 'EasyVisa.csv'
MODEL_FILE_NAME = 'model.pkl'


TARGET_COLUMN = 'case_status'
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME = 'preprocessing.pkl'
SCHEMA_FILE_PATH = os.path.join('config', 'schema.yaml')


DATA_INGESTION_COLLECTION_NAME: str = 'Visa'
DATA_INGESTION_DIR_NAME:str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR:str = 'feature_store'
DATA_INGESTION_INGESTED_DIR:str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2

DATA_VALIDATION_DIR_NAME:str = 'data_validation'
DATA_VALIDATION_DRIFT_REPORT_DIR:str = 'drift_report'
DATA_VALIDATION_DRIFR_REPORT_FILE_NAME:str = 'report.yaml'