from typing import Dict, List

from pymongo import MongoClient
from pymongo.collection import Collection



class MongoDBManager():
    def __init__(self, url: str, db_name: str) -> None:
        self.client = MongoClient(url, serverSelectionTimeoutMS=5000)
        self.database = self.client[db_name]
        self.collection = None

    def ping(self):
        self.client.server_info()
    
    def set_collection(self, collection_name: str) -> Collection:
        self.collection = self.database[collection_name]
    
    def get_all_data_from_collection(self, collection_name: str, filter: Dict = None) -> List[Dict]:
        self.set_collection(collection_name)
        return list(self.collection.find({}, filter))

    def get_one_data_from_collection(self, collection_name: str, filter: Dict):
        self.set_collection(collection_name)
        return self.collection.find(filter)
    
    def add_data_to_collection(self, collection_name: str, data: Dict):
        self.set_collection(collection_name)
        self.collection.insert_one(data)

    def update_one_data_from_collection(self, collection_name: str, filter: Dict, update_values: Dict):
        self.set_collection(collection_name)
        self.collection.update_one(filter=filter, update=update_values)

    def remove_one_data_from_collection(self, collection_name: str, filter: Dict):
        self.set_collection(collection_name)
        self.collection.delete_one(filter)

    def drop_data_from_collection(self, collection_name: str):
        self.set_collection(collection_name)
        self.collection.delete_many({})
