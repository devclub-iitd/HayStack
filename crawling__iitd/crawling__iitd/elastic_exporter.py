from logging import warn
from typing import overload
from scrapy.exporters import BaseItemExporter
from elasticsearch import helpers, Elasticsearch
from elasticsearch.helpers import  streaming_bulk,bulk
from multiprocessing import Queue, Process, log_to_stderr
from datetime import datetime
import warnings
import logging

#from crawler.config import ELASTIC_URI, ELASTIC_INDEX_NAME, mongo_collection
from crawling__iitd.mongo_creator import getMongoCollection
from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection


ELASTIC_URI ="localhost:9200"
ELASTIC_INDEX_NAME = "iitd_sites"
class ElasticExporter(BaseItemExporter):
    
    def __init__(self, _, **kwargs) -> None:
        super().__init__(dont_fail=True, **kwargs)


    def start_exporting(self):
        self.client = Elasticsearch([ELASTIC_URI])
        self.mongo_collection: Collection = getMongoCollection()
        if not self.client.indices.exists(ELASTIC_INDEX_NAME):
            self.client.indices.create(ELASTIC_INDEX_NAME)
        
        #for bulk export to ES
        self.list=[]
    
    def finish_exporting(self):
        bulk(self.client,self.list)
        print("exporting process ended")
        
    
    def export_item(self, item):
        response_url = item["url"]
        response_title=item["title"]
        response_body=item["body"]
        #IDEAL FIELDS FOR SEARCH RESULTS # self.list.append({"_index":"iitd_sites","_type":'_doc', "url":response_url,"title":response_title,"body":response_body})#{'link':response_url,'title':response_title, "body":response_body}})

        #for bulk export
        if not self.client.exists(index=ELASTIC_INDEX_NAME, id=response_url):
            #print("****************************|| CONDITION PASSED ||***********************************")
            self.list.append({"_index":"iitd_sites",
                          "_type":"_doc",
                          "_id":response_url,
                          "url":response_url,
                          "title":response_title,
                          "body":response_body,
                          "meta_data":item["meta_data"],
                          "links_text":item["links_text"],
                          "links_url":item["links_url"],
                          "linked_img":item["image_urls"],
                          "visits":0
                        })
        
        print("list lenth changed to ",len(self.list))
        if (len(self.list)>=5):
            bulk( self.client , self.list )
            #self.client.indices.refresh("iitd_sites")
            for data in self.list:
                if self.client.exists(index="iitd_sites", id=data["url"]):
                    self.mongo_collection.update_one({"url": data["url"]},
                                                     {"$set": {"indexed":True}},
                                                     upsert=True,
                                                    )
            self.list.clear()        
        
       
        #condition to be added
        #self.client.index(index='iit',doc_type='_doc',body={'url':response_url,'title':response_title, "body":response_body})
        
        
        # self.mongo_collection.update_one(
        #     {"url": response_url},
        #     {
        #         "$set": {"indexed":True}
        #     },
        #     upsert=True,
        # )

       