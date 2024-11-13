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


AWS_ACCESS_KEY_ID_ENV_KEY = 'AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY_ENV_KEY = 'AWS_SECRET_ACCESS_KEY'
REGION_NAME = 'us-east-1'


DATA_INGESTION_COLLECTION_NAME: str = 'Visa'
DATA_INGESTION_DIR_NAME:str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR:str = 'feature_store'
DATA_INGESTION_INGESTED_DIR:str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2

DATA_VALIDATION_DIR_NAME:str = 'data_validation'
DATA_VALIDATION_DRIFT_REPORT_DIR:str = 'drift_report'
DATA_VALIDATION_DRIFR_REPORT_FILE_NAME:str = 'report.yaml'

DATA_TRANSFORMATION_DIR_NAME:str = 'data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = 'transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = 'transformed_object'


MODEL_TRAINER_DIR_NAME:str = 'model_trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR:str = 'trained_model'
MODEL_TRAINER_TRAINED_MODEL_NAME:str = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_NAME:str = os.path.join('config','model.yaml')


MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE:float =0.02
MODEL_BUCKET_NAME = 'usvisa-model'
MODEL_PUSHER_S3_KEY = 'model-registry'


APP_HOST = '0.0.0.0'
APP_PORT = 8000