# IITD_SearchEngine
This repository contains a search engine for domain "iitd.ac.in"


As of 29th November 2021

Branch storing_files has the latest working code

python modules required
-scrapy
-elasticsearch
-textract
-datetime

to start frontend - commands to be executed in search_frontend directory
-npm ci
-npm run start

to start the crawler
-run the main.py file in crawling_iitd


elastic_search index = iitd_sites

Crawler limit - 20000 pages
Elastic Bulk export for every 100 pages

Functionality enabled to limit the no. of requests made to iitd.ac.in per second


Issues
-Visits of a page are not getting updated