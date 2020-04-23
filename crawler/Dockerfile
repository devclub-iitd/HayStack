FROM python:3.8.2-alpine3.11

RUN mkdir /crawler
WORKDIR /crawler

RUN apk add --update --no-cache g++ gcc libxslt-dev curl
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir 

COPY . .
CMD ["/bin/sh", "-c" , "/crawler/entrypoint.sh"] 
