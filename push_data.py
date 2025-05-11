import sys
import os
import json

from dotenv import load_dotenv
import pymongo.mongo_client
load_dotenv

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca=certifi.where()

import numpy as np
import pandas as pd
import pymongo
from networksecurity.exception.exception_handling import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def csv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)

            # Convert to JSON string in records orientation
            json_str = data.to_json(orient='records')

            # Convert JSON string to Python list of dicts
            records = json.loads(json_str)

            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)

            self.database=self.mongo_client[self.collection]
            self.collection=self.database[self.collection]

            self.collection.insert_many(self.records)

            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)


if __name__=="__main__":
    FILE_PATH="Netwrok_Data\phisingData.csv"
    DATABASE="Mudaseer"
    Collection="NetworkData"
    networKobj=NetworkDataExtract()
    records=networKobj.csv_to_json_convertor(file_path=FILE_PATH)
    no_of_records=networKobj.insert_data_mongodb(records=records,database=DATABASE,collection=Collection)
    print(no_of_records)