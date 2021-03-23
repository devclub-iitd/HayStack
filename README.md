# Haystack: A search engine built for IIT Delhi - quickly search across all official IITD Webpages!

##
<img width="600" alt="Screen Shot 2021-02-02 at 4 06 29 AM" src="https://user-images.githubusercontent.com/54809290/106526743-233ac880-650c-11eb-96bb-583f5d2ffdc1.png">

## :star: Features

- Search through all .iitd.ac.in websites

## :computer: Getting Started

### Prerequisites
- Docker

### :arrow_forward: Start

```sh
docker-compose up --build -d -t 500

cd search_frontend
npm ci
npm install react-scripts@3.0.1 -g
npm run start
```

**Note:** We specify a high timeout because on receiving SIGINT, the app attempts to
complete all pending requests and flush them to appropriate databases.


## :building_construction: Built With

- Front End
  - [:link: ReactJS](https://github.com/facebook/react)
- Back End
  - [:link: Scrapy](https://github.com/scrapy/scrapy)
  - [:link: MongoDB](https://github.com/mongodb/mongo)
  - [:link: Elasticsearch](https://github.com/elastic/elasticsearch)


## :clipboard: Known Issues
...


<!-- ## Crawler working

We use a Scrapy Spider to crawl webpages, with the initial seed as iitd.ac.in.

We store all data related to pages we've crawled in a database using MongoDB. We
use Mongo instead of a simple text file or in memory array so we can resume our
crawl when we restart, scale better, and perhaps even re-crawl sites which were
crawled before a particular date. -->


## :busts_in_silhouette: Contributors
| [<img src="https://github.com/arpit-saxena.png" width="100px;"/>](https://github.com/arpit-saxena)<br/> [<sub>Arpit Saxena</sub>](https://github.com/arpit-saxena) |
| --- |
| [<img src="https://github.com/JapneetSingh5.png" width="100px;"/>](https://github.com/JapnneetSingh5)<br/> [<sub>Japneet Singh</sub>](https://github.com/japeetsingh5) |


## :copyright: License
This project is licensed under the MIT License.
