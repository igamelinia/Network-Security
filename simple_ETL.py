import os 
import sys
import json

# How to get key in .env
from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")

# Make sure there is no certification SSL error
import certifi
ca=certifi.where()

import pandas as pd 
import numpy as np
import pymongo
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging

# Create Class for simple ETL 
class NetworkDataETL():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys)
        
    def csv_to_json_convertor(self, file_path):
        try :
            data=pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise CustomException(e, sys)
        
    def insert_data_mongodb(self, records, database, collection):
        try :
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))

        except Exception as e:
            raise CustomException(e, sys)
        


if __name__=='__main__':
    FILE_PATH="Network_Dataset\phisingData.csv"
    DATABASE="MELINIA"
    collection="NetworkData"
    network_obj=NetworkDataETL()
    records = network_obj.csv_to_json_convertor(FILE_PATH)
    numbers_records = network_obj.insert_data_mongodb(records=records,
                                                    database=DATABASE,
                                                    collection=collection)
    print(numbers_records)