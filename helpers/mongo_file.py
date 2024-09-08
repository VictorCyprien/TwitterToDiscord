from typing import Dict

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor



class MongoDBManager():
    def __init__(self, url: str, db_name: str) -> None:
        self.client = MongoClient(url)
        self.database = self.client[db_name]
        self.collection = None
    
    def set_collection(self, collection_name: str) -> Collection:
        self.collection = self.database[collection_name]
    
    def get_all_data_from_collection(self) -> Cursor:
        return self.collection.find()

    def get_one_data_from_collection(self, filter: Dict):
        return self.collection.find(filter)

    def update_one_data_from_collection(self, filter: Dict, update_values: Dict):
        self.collection.find_one_and_update(filter, update_values)

    def remove_one_data_from_collection(self, filter: Dict):
        self.collection.find_one_and_delete(filter)
