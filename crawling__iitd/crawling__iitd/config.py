"""#dotenv not working properly.... need to be resolved.# """


import os
#from dotenv import load_dotenv
import crawling__iitd.mongo_creator as utils

#load_dotenv()

MONGODB_URI = "mongodb://localhost:27170"

if MONGODB_URI is None:
    raise Exception('MONGODB_URI not set')

MONGO_DBNAME =  'haystack'
MONGO_COLLNAME = 'crawl_info'

mongo_collection = utils.getMongoCollection()