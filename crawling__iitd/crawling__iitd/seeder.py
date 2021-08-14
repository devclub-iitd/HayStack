from multiprocessing import Process, Queue, log_to_stderr
import signal
import logging
from crawling__iitd.config import MONGODB_URI, MONGO_DBNAME, MONGO_COLLNAME
from pymongo.mongo_client import MongoClient

class Seeder():
    def __init__(self, mongo_collection, query=None) -> None:
        if query is None:
            query = {
                "scraped": {
                    "$eq": False,
                }
            }
        self.query = query
        self.mongo_collection = mongo_collection

    def seed(self) -> None:
        for doc in self.mongo_collection.find(self.query):
            yield doc