# IITD_SearchEngine
This repository contains a search engine for domain "iitd.ac.in"

As of 26th December 2021

Branch dev has the latest working code for deployment

A .env file needed in [Crawler/crawling__iitd/crawling__iitd] having the following contents
ELASTIC_URL='elastic:9200'
ELASTIC_INDEX_NAME='iitd_sites'

To run -
docker-compose up --build

Crawler limit - 20000 pages
Elastic Bulk export for every 10 pages

Functionality enabled to limit the no. of requests made to iitd.ac.in per second

python modules required
-scrapy
-elasticsearch
-textract
-datetime
-python-dotenv