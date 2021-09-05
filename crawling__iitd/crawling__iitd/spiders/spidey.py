#-*-coding: utf-8-*-
import scrapy
import sys
import re
import textract
from itertools import chain
from tempfile import NamedTemporaryFile
#sys.path.insert(0,'/Documents/haystack/new/crawling__iitd/elastic_eporter.py')
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawling__iitd.items import CrawlingIitdItem, CrawlingIitdItemLoader 
import time

LST=[".pdf",".doc",".docx"] #the list can be extended to make crawler crawl links with another extensions
class CustomLinkExtractor(LinkExtractor):
    def __init__(self,*args, **kwargs):       
        super(CustomLinkExtractor,self).__init__(*args,**kwargs)
        self.deny_extensions=[ext for ext in self.deny_extensions if ext not in LST] #print self.deny_extensions to get the list of extension that cannot be crawled.


class IITDSpider (CrawlSpider):
    name = 'IITD' # crawler name
    allowed_domains = [
        'iitd.ac.in',
        'iitd.ernet.in'
    ]
    start_urls = ['https://home.iitd.ac.in/'] 

    rules = (
        #Configure the crawl list page rule
        Rule (CustomLinkExtractor(), callback="parse_job",follow = True),

        #Configure rules for crawling content pages
        Rule (CustomLinkExtractor(), callback ="parse_job", follow = True),)

    def parse_job (self, response):
        if hasattr(response, "text"):

            # The response is text - we assume html.
            #atime = time.localtime (time.time ()) #Get the current system time
            # dqatime = "{0}-{1}-{2} {3}: {4}: {5}". format (
            #     atime.tm_year,
            #     atime.tm_mon,
            #     atime.tm_mday,
            #     atime.tm_hour,
            #     atime.tm_min,
            #     atime.tm_sec
            # ) # The formatted date and time are taken out separately and stitched into a complete date
            linked_images=response.css('img ::attr(src)').getall()
            links_url=response.css('a::attr(href)').extract()
            links_text=response.css('a::text').extract()
            link_dict=self.extract_links(response,links_url,links_text)
            body=self.extract_body(response)
            clean_link_img={"img":[]}
            for img in linked_images:
                clean_link_img["img"].append(response.urljoin(img))
            whole_body=''
            for i in body:
                whole_body+=i

            url = response.url
            print("-----------------------------------------","\n")
            print(url)
            print("-----------------------------------------",'\n')
            item_loader = CrawlingIitdItemLoader(CrawlingIitdItem(), response = response) # Fill the data into the CrawlingIitdItem of the items.py file
            item_loader.add_xpath('title', '/ html / head / title / text ()')
            item_loader.add_value('url', url)
            item_loader.add_value('body',whole_body)
            item_loader.add_value('linked_urls', link_dict)
            item_loader.add_value('linked_images',clean_link_img)
            item_loader.add_css('meta_tags','meta')
            #item_loader.add_value('riqi', dqatime)
            article_item = item_loader.load_item ()

            yield article_item
        else:
            
            # We assume the response is binary data                                                                                                                                                
            control_chars = ''.join(map(chr, chain(range(0, 9), range(11, 32), range(127, 160))))
            CONTROL_CHAR_RE = re.compile('[%s]' % re.escape(control_chars))
            # One-liner for testing if "response.url" ends with any of TEXTRACT_EXTENSIONS                                                                                                         
            extension = list(filter(lambda x: response.url.lower().endswith(x), LST))[0]
            if extension:
                # This is a pdf or something else that Textract can process                                                                                                                        
                # Create a temporary file with the correct extension.                                                                                                                              
                tempfile = NamedTemporaryFile(suffix=extension)
                tempfile.write(response.body)
                tempfile.flush()
                extracted_data = textract.process(tempfile.name)
                extracted_data = extracted_data.decode('utf-8')
                extracted_data = CONTROL_CHAR_RE.sub('', extracted_data)
                tempfile.close()
		        
                #for checking whether the pdf data is being stored or not.
                # with open("scraped_content.txt", "a") as f:
                #     f.write(response.url.upper())
                #     f.write("\n")
                #     f.write(extracted_data)
                #     f.write("\n\n")

                doc_link_dict={}
                doc_clean_link_img={"img":[]}
                doc_item_loader = CrawlingIitdItemLoader(CrawlingIitdItem()) # Fill the data into the CrawlingIitdItem of the items.py file
                doc_item_loader.add_value('title', "PDF-"+extracted_data[0:8])
                doc_item_loader.add_value('linked_urls', doc_link_dict)
                doc_item_loader.add_value('linked_images',doc_clean_link_img)
                doc_item_loader.add_value('url', response.url)
                doc_item_loader.add_value('body',extracted_data)
                
                #item_loader.add_value('riqi', dqatime)
                doc_article_item = doc_item_loader.load_item ()

                yield doc_article_item
    
    def extract_links(self,response,links_url,links_text):
        links={
            "pdf":[],
            "ppt":[],
            "text":[],
            "spreadsheet":[],
            "programs":[],
            "webpages":[]
            }

        keys=["pdf","ppt","text","spreadsheet","programs"]

        formats=[
            [".pdf"],
            [".pptx",".ppt",".pptm",".potx",".pot",".potm",".pps",".ppsm",".ppsx"],
            [".docx",".txt",".doc",".docm"],
            [".csv",".xla",".xls",".xlsm",".xlsx",".xlt","xltx","xltm"],
            [".c",".cpp",".java",".py"]
            ]

        for (text,link) in zip(links_text,links_url):
            link=link.rstrip(' ')
            link=link.lstrip(" ./")
            if not link.startswith("http"):
                link=response.url+"/"+link
            found=False
            index=0
            for x1 in formats:
                key=keys[index]
                index+=1
                for x2 in x1:
                    found=False
                    if link.endswith(x2):
                        found=True
                        links[key].append({"text":text,"link":link})
                        break
                if found:
                    break
            
            if not found:
                links["webpages"].append({"text":text,"link":link})
        return links
        

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