from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
import crawler.config as config


def getMongoCollection() -> Collection:
    client = MongoClient(host=config.MONGODB_URI)
    db = client[config.MONGO_DBNAME]
    collection = db[config.MONGO_COLLNAME]
    return collection
