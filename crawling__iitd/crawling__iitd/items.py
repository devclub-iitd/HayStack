# Define here the models for your scraped items
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import sys
import os
import itemloaders
import scrapy
from elasticsearch import helpers, Elasticsearch
from elasticsearch.helpers import bulk
#from elasticsearch_dsl.connections import connections
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from scrapy.loader import ItemLoader #Import the ItemLoader class and load the items container class to fill the data
#import ItemLoader.processors.TakeFirst

class CrawlingIitdItemLoader(ItemLoader): #Custom Loader inherits ItemLoader class, call this class on the crawler page to fill the data to Item class
    default_output_processor = itemloaders.processors.TakeFirst() #The ItemLoader class is used by default to load the items container class to fill the data. It is a list type. You can get the contents of the list through the TakeFirst () method


def tianjia(value): #Custom data preprocessing function
    return value #Return the processed data to the Item. Currently the data processing is being done in spidey.py file so nothing special to write here, just returning the values here.

bulk_lst=[] #for bulk indexing in ES using a list of documnets(i.e. list of Item with some extra fields) <blk_lst>
host='localhost:9200'
ELASTIC_INDEX_NAME="iitd_sites"
class CrawlingIitdItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field (#Receive title information obtained by the crawler
        input_processor = itemloaders.processors.MapCompose(tianjia), #Demo of data processing application in fields of Item.Pass the data preprocessing function name into the MapCompose method for processing. The formal parameter value of the data preprocessing function will automatically receive the field title   
    )
    url = scrapy.Field ()
    body = scrapy.Field ()
    linked_urls = scrapy.Field ()
    linked_images = scrapy.Field ()
    meta_tags = scrapy.Field ()

    def save_to_es (self,item): #function for saving the data stored in Item of every crawled webpage to ES
        
        #if-else coditions are required as some of the crawled urls(webpages) don't have some of the fields in their Item. 
        response_url = item["url"]
        if "title" in item.keys(): 
            response_title=item["title"]
        else:
            response_title=item["body"][:10]
        
        response_body=item["body"]

        if "linked_images" in item.keys():
            response_images=item["linked_images"]
        else:
            response_images={"img":[]}

        if "linked_urls" in item.keys():
            response_links=item["linked_urls"]
        else:
            response_links={}

        if "meta_tags" in item.keys():
            response_meta=item["meta_tags"]
        else:
            response_meta=""
        #print(item)
        
        es_client=Elasticsearch(host)
        if not es_client.indices.exists(ELASTIC_INDEX_NAME):
            es_client.indices.create(ELASTIC_INDEX_NAME)#initialise index with index_name=elastic_index_name

        es_client.indices.refresh(ELASTIC_INDEX_NAME) #to get the count of documents indexed in "iitd-sites" on ES, refreshing is required.
        es_len=es_client.cat.count(ELASTIC_INDEX_NAME, params={"format": "json"})
        
        if int(es_len[0]['count'])>100: #you can define total number of documents you want to index in ES
            print("100 DOCUMENTS INDEXED--------------","\n")
            os._exit(0)
        
        if not es_client.exists(index=ELASTIC_INDEX_NAME, id=response_url):
            bulk_lst.append({"_index":"iitd_sites",
                          "_type":"_doc",
                          "_id":response_url,
                          "url":response_url,
                          "title":response_title,
                          "body":response_body,
                          "links":response_links,
                          "linked_images":response_images,
                          "meta_data":response_meta,
                          "visits":0
                        })

        if len(bulk_lst)>=10:
            bulk(es_client,bulk_lst)
            bulk_lst.clear()
            return
        else:
            pass  
    