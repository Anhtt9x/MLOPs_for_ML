from US_visa.configuration.mongodb_connection import MongoDBClient
from US_visa.constants import *
from US_visa.exception import USvisaException
import pandas as pd
import sys
from typing import Optional
import numpy as np

class USvisaData:
    def __init__(self):
        try:
            self.mongoclient = MongoDBClient(database_name=DATABASE_NAME)

        except Exception as e:
            raise USvisaException(e,sys)
        
    
    def export_collection_dataframe(self,collection_name:str,database_name:Optional[str]=None) -> pd.DataFrame:
        try:
            if database_name is None:
                collection = self.mongoclient.database[collection_name]
            else:
                collection = self.mongoclient[database_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))
            if '_id' in df.columns.tolist():
                df=df.drop(columns='_id', axis=1)
            
            df.replace({'na':np.nan}, inplace=True)
            return df
        except Exception as e:
            raise USvisaException(e,sys)
