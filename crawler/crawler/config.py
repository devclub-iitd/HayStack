"""
Common configuration file for all modules to share

Queues:
- crawl_queue: A scrapy spider consumes from this queue and crawls these URLs

- fetched_doc_queue: Responses from the crawled URLs are inserted by the spider
  into this queue. This queue will be iterated by ElasticSearch's bulk inserter.

"""

import os
from dotenv import load_dotenv
import crawler.utils as utils

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
if MONGODB_URI is None:
    raise Exception('MONGODB_URI not set')

MONGO_DBNAME = os.getenv('MONGO_DBNAME', 'haystack')
MONGO_COLLNAME = os.getenv('MONGO_COLLNAME', 'crawl_info')

ELASTIC_URI = os.getenv('ELASTIC_URI')
if ELASTIC_URI is None:
    raise Exception('ELASTIC_URI not set')
ELASTIC_INDEX_NAME = os.getenv('ELASTIC_INDEX_NAME', 'iitd_sites')

mongo_collection = utils.getMongoCollection()
