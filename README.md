# Haystack
This repository contains a search engine for domain "iitd.ac.in"

To run - 'docker-compose up --build'

Crawler limit - 20000 pages
Elastic Bulk export for every 100 pages

Functionality enabled to limit the no. of requests made to iitd.ac.in per second

##### python modules required
- scrapy
- elasticsearch
- textract
- datetime

##### Required URLs for 
- Crawler specified in - Crawler/crawling__iitd/crawling__iitd/params.py
- nginx - nginx/nginx.conf
- search_frontend - search_frontend/Dockerfile

##### Nginx configuration 
- / - passes request to frontend
- /iitd_sites - passes request to Elasticsearch


##### Nginx listens on port 7000, to change - 
- change REACT_APP_ELASTIC_URL in search_frontend/Dockerfile
- change port in Nginx service in docker-compose.yml
