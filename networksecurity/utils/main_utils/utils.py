import yaml
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
import os 
import sys
import numpy as np 
import pickle

# Function for read yaml_file
def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            # safe_load for avoid from execute danger data in yaml file
            return yaml.safe_load(yaml_file)
    except Exception as e :
        raise CustomException(e,sys)

# Fuction for write yaml file
def write_yaml_file(file_path:str, content: object, replace:bool = False) -> None:
    try:
        if replace :
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e :
        raise CustomException(e, sys)
    
# Fuction for save numpy array data 
def save_numpy_array_data(file_path:str, array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, array)
    except Exception as e:
        raise CustomException(e,sys)

# Function for save object like preprocessor and model pkl
def save_object(file_path:str, obj:object):
    try:
        logging.info("Entered the Save Object method of Main_utils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the Save Object method")

    except Exception as e:
        raise CustomException(e, sys)
