import sys
from US_visa.exception import USvisaException
from US_visa.logger import logging
import os
from US_visa.constants import * 
import pymongo
import certifi

ca = certifi.where()

class MongoDBClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME):
        try:
            if MongoDBClient.client is None:
                mongodb_url = MONGODB_URL_KEY
                if mongodb_url is None:
                    raise Exception(f"{MONGODB_URL_KEY} is not set")
                MongoDBClient.client = pymongo.MongoClient(mongodb_url, tlsCAFile=ca)

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info(f"MongoDB client created for database: {database_name}")
        except Exception as e:
            raise USvisaException(e, sys)
        

if __name__ == "__main__":
    client = MongoDBClient()