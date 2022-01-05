#!/bin/bash

until nc -z -v "elastic" 9200; do
    echo "Waiting for ElasticSearch";

    sleep 10;
done

exec python crawling__iitd/main.py