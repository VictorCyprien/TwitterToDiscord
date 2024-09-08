from typing import Dict, List

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor



class MongoDBManager():
    def __init__(self, url: str, db_name: str) -> None:
        self.client = MongoClient(url, serverSelectionTimeoutMS=5000)
        self.database = self.client[db_name]
        self.collection = None

    def ping(self):
        self.client.server_info()
    
    def set_collection(self, collection_name: str) -> Collection:
        self.collection = self.database[collection_name]
    
    def get_all_data_from_collection(self) -> List[Dict]:
        return list(self.collection.find())

    def get_one_data_from_collection(self, filter: Dict):
        return self.collection.find(filter)
    
    def add_data_to_collection(self, data: Dict):
        self.collection.insert_one(data)

    def update_one_data_from_collection(self, filter: Dict, update_values: Dict):
        self.collection.find_one_and_update(filter, update_values)

    def remove_one_data_from_collection(self, filter: Dict):
        self.collection.find_one_and_delete(filter)

    def drop_data_from_collection(self):
        self.collection.delete_many({})
