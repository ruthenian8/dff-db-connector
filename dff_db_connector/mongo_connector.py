import json
from functools import wraps
from typing import Callable
from bson.objectid import ObjectId

from pymongo import MongoClient

from .dff_db_connector import DffDbConnector
from df_engine.core.context import Context


class MongoConnector(DffDbConnector):
    def __init__(self, path: str, collection: str = "context_collection"):
        super(MongoConnector, self).__init__(path)
        self._mongo = MongoClient(self.full_path)
        db = self._mongo.get_default_database()
        self.collection = db[collection]

    @staticmethod
    def adjust_key(key: str):
        """Convert a 9-digit telegram user id to a 20 digit mongo id"""
        new_key = key + "0" * (24 - len(key))
        assert len(new_key) == 24
        return {"_id": ObjectId(new_key)}

    def __setitem__(self, key: str, value: Context) -> None:
        key = self.adjust_key(key)
        value_dict = value.dict()
        value_dict.update(key)
        self.collection.replace_one(key, value_dict, upsert=True)

    def __getitem__(self, key: str) -> Context:
        key = self.adjust_key(key)
        value = self.collection.find_one(key)
        if value:
            return value
        raise KeyError

    def __delitem__(self, key: str) -> None:
        key = self.adjust_key(key)
        self.collection.delete_one(key)

    def __contains__(self, key: str) -> bool:
        key = self.adjust_key(key)
        return bool(self.collection.find_one(key))

    def __len__(self) -> int:
        return self.collection.estimated_document_count()

    def __del__(self) -> None:
        self._mongo.close()
