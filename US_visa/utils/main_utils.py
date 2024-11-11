import os
import sys

import numpy as np
import dill
import yaml
from pandas import DataFrame

from US_visa.exception import USvisaException
from US_visa.logger import logging

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
        
    except Exception as e:
        raise USvisaException(e,sys) from e
    

def write_yaml_file(file_path:str, content:object, replace:bool=False) ->  None:
    try:
        if replace:
            if  os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path,"w") as file:
            yaml.dump(content, file)
    
    except Exception as e:
        raise USvisaException(e,sys) from e
    

def load_object(file_path:str) -> object:
    logging.info("Entered the load object method of utils")

    try:
        with open(file_path, "rb") as file:
            return dill.load(file)
        logging.info("Exited the load object method")
    
    except Exception as e:
        raise USvisaException(e,sys) from e
    

def save_numpy_array_data(file_path:str, array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file:
            np.save(file, array)
    except Exception as e:
        raise USvisaException(e,sys) from e

    
def load_numpy_array_data(file_path:str) -> np.array:
    try:
        with open(file_path,'rb') as file:
            return np.load(file)
        
    except Exception as e:
        raise USvisaException(e,sys) from e
    

def save_object(file_path:str, obj:object) -> None:
    logging.info("Entered the save object method of utils")
    try:
        os.makedirs(os.path.dirname(file_path),  exist_ok=True)
        with open(file_path,"wb") as file:
            dill.dump(obj, file)
        logging.info("Exited the save object method of utils")

    except Exception as e:
        raise USvisaException(e,sys) from e
    

def drop_columns(df:DataFrame, cols:list) -> DataFrame:
    logging.info("Entered drop columns method of utils")
    try:
        return df.drop(columns=cols)
        logging.info("Exited the drop columns method of utils")
    except Exception as e:
        raise USvisaException(e,sys) from e
    
    