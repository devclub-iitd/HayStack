from logging import warn
from typing import overload
from scrapy.exporters import BaseItemExporter
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from multiprocessing import Queue, Process, log_to_stderr
from datetime import datetime
import warnings
import logging

from crawler.config import ELASTIC_URI, ELASTIC_INDEX_NAME, mongo_collection
from crawler.utils import getMongoCollection

def snoop_queue(mongo_collection, queue: Queue, logger: logging.Logger):
    """
    Takes in items from the multiprocessing queue and yields them so that they
    can consumed by streaming_bulk. After that, that item's status is updated in
    mongo
    """

    for item in iter(queue.get, None):
        yield item

        mongo_collection.find_one_and_update(
            {"url": item["url"]},
            {
                "$push": {
                    "crawl_details": {
                        "crawled_on": datetime.utcnow(),
                        "response_code": item["status"],
                    }
                }
            },
            upsert=True,
        )



def inserter(client, queue):
    mongo_collection = getMongoCollection()
    logger = log_to_stderr()
    logger.setLevel(logging.INFO)

    logger.info("Started ElasticSearch insertion process")
    for ok, action in streaming_bulk(
        client=client,
        index=ELASTIC_INDEX_NAME,
        actions=snoop_queue(mongo_collection, queue, logger),
        max_retries=5,
        chunk_size=50,
    ):
        pass
        


class ElasticExporter(BaseItemExporter):

    def __init__(self, _, **kwargs) -> None:
        super().__init__(dont_fail=True, **kwargs)

    def start_exporting(self):
        self.client = Elasticsearch([ELASTIC_URI])

        if not self.client.indices.exists(ELASTIC_INDEX_NAME):
            self.client.indices.create(ELASTIC_INDEX_NAME)

        self.queue = Queue()
        self.inserter_process = Process(
            target=inserter, args=(self.client, self.queue))
        self.inserter_process.start()

    def finish_exporting(self):
        self.queue.put(None)
        self.inserter_process.join()

    def export_item(self, item):
        # Used by elastic search's streaming_bulk. It will update mongo once the
        # doc has been inserted
        self.queue.put(item["elastic_doc"])

        # logging.warn(item["request"].meta)

        response_url = item["elastic_doc"]["url"]
        request_doc = item["request"].meta["mongo_doc"]
        request_url = request_doc["url"]

        # If request_url is not same as response_url, there must have been a
        # redirect

        if request_url != response_url:
            redirect_reasons = []
            if "redirect_reasons" in item["request"].meta:
                redirect_reasons = item["request"].meta["redirect_reasons"]

            # These URLs can differ without any id difference due to presence of
            # #ids
            if len(redirect_reasons) == 0:
                status = 300
            else:
                # FIXME: This may contain a "meta-refresh" string, but our db
                # expects an int. Also, can we use the redirect chain somehow?
                status = redirect_reasons[0] if isinstance(
                    redirect_reasons[0], int) else 300

            mongo_collection.find_one_and_update(
                {"_id": request_doc["_id"]},
                {
                    "$push": {
                        "crawl_details": {
                            "crawled_on": datetime.utcnow(),
                            "response_code": status,
                        }
                    }
                },
                upsert=True
            )
