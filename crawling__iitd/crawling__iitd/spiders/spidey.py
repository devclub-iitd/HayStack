import datetime
from scrapy import signals
from scrapy.http import Request, Response
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pymongo.collection import Collection, ReturnDocument
from crawling__iitd.seeder import Seeder
from crawling__iitd.mongo_creator import getMongoCollection

class IITDSpider(CrawlSpider):
    name = "iitd"

    allowed_domains = [
        'iitd.ac.in',
        'iitd.ernet.in'
    ]

    rules = [
        Rule(LinkExtractor(), follow=True, callback="parse_item",process_request="process_request")
    ]

    start_urls = [
        'https://home.iitd.ac.in',
    ]

    #start_request generates request for all links
    def start_requests(self):
        self.mongo_collection: Collection = getMongoCollection()
        for url in self.start_urls:
            doc = self.mongo_collection.find_one_and_update({"url": url}, {"$setOnInsert": {
                "crawl_details": {},
                "scraped": False,
                "indexed":False}
                }, upsert=True, return_document=ReturnDocument.AFTER)
        
        #seeder returns the crawl_info collection...so that Request could be yielded for priviosly crawled links(doc).
        #initially crawl_info does not contain any data ...
        for doc in Seeder(self.mongo_collection).seed():
            url = doc['url']
            self.logger.info(f"Got {url} from seeder")
            yield Request(url, meta={"mongo_doc": doc})


    def process_request(self, request: Request, response: Response):
        self.logger.debug('Processing request')
        print("--------------------------------------------","\n")
        #newly visited links would not have mongo_doc in request.meta....so saving them in crawl_info ...once saved ...Request would be created for them and hence mongo_doc will then be present in request.meta
        if "mongo_doc" not in request.meta:
            request.meta["mongo_doc"] = self.mongo_collection.find_one_and_update({"url": request.url},{"$setOnInsert": {
                "crawl_details": {},
                "scraped": False,
                "indexed":False}
                },upsert=True,return_document=ReturnDocument.AFTER)

        #Drop this request if it has already been crawled
        # if len(request.meta["mongo_doc"]["crawl_details"]) != 0:
        if request.meta["mongo_doc"]["scraped"]!=False:
            return None
        
        return request
    
    # def parse_item(self, response):
    #     self.logger.info('Hello World Checking this function')
    #     item = {
    #         "request": response.request,
    #         "elastic_doc": {
    #             'url': response.url,
    #             'status': response.status,
    #             'title': response.xpath("//title").get(),
    #             'body': response.xpath("//body").get(),
    #             'link_text': response.meta['link_text'],
    #         },
    #     }

    #     return item

    def parse_item(self,response) :
        if response.status==200:
            self.logger.info(f'Scraping Page with url {response.url}')
            body=self.extract_body(response)

            link_img=response.css('img ::attr(src)').getall()
            clean_link_img=[]
            links=response.css('a')
            links_url=links.css('::attr(href)').extract()
            links_text=links.css('::text').extract()
            remove='\n \t \f \r \b'
            for text in links_text:
                text=text.lstrip(remove)
                text=text.rstrip(remove)

            for img in link_img:
                clean_link_img.append(response.urljoin(img))
                
            item = {
                "url":response.url,    
                "status":response.status,
                "title":response.css('title::text').get(),
                "meta_data":response.css('meta').extract(),
                "body":body,
                "image_urls":clean_link_img,
                "crawled_on":datetime.datetime.now(),
                "links_url":links_url,
                "links_text":links_text,
            }
            # doc = self.mongo_collection.find_one_and_update({"url": response.url},{"$setOnInsert": {"crawl_details": item,"crawled_on": datetime.datetime.now()}},upsert=True,return_document=ReturnDocument.AFTER)
            myquery = { 'url': response.url }
            newvalues = { "$set": {'scraped':True } }
            self.mongo_collection.update_one(myquery, newvalues)
            
            yield item 
        else:
            yield None

    def extract_body(self,response):
        body=[]
        # cheking for paragraphs
        paras=response.css('p::text').extract()
        wrd_count=0
        for str in paras :
            val=self.check_string(str)
            if(val==-1):
                paras.remove(str)
            else:
                wrd_count+=val
        if (wrd_count>25):
            return paras
        else:
            # if no element of very less number of words are these in paras, then it is concatenated with headings and bolds tags.
            body+=paras

        # checking for headings <h2>
        headings=response.css('h2::text').extract()
        for str in headings:
            val=self.check_string(str)
            if(val==-1):
                headings.remove(str)
            else:
                wrd_count+=val
        body+=headings
        if (wrd_count>25):
            return body

        # checking for bolds tags
        bolds=response.css('b::text').extract()
        for str in bolds:
            val=self.check_string(str)
            if(val==-1):
                bolds.remove(str)
            else:
                wrd_count+=val
        body+=bolds
        if wrd_count>2:
            return body
        
        # none found
        return ['No information is available regarding body']

    def check_string(self,str):
        remove="\n \t \f \r \b  "
        str=str.lstrip(remove)
        str=str.rstrip(remove)
        if(len(str)<=2):
            return -1
        else:
            count=0  # counting number of spaces to get an estimate of number of words
            for c in str:
                if(c==' '):
                    count+=1
            if(count<4):
                return -1
            else:
                return count
