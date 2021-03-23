#!/bin/sh

until nc -z "mongo" 27017; do
	echo "Waiting for MongoDB";
	sleep 10;
done

until nc -z "elastic" 9200; do
    echo "Waiting for ElasticSearch";
    sleep 10;
done

exec scrapy crawl iitd