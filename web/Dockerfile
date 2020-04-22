FROM python:3.8.2-alpine3.11

RUN mkdir /web
WORKDIR /web
ENV FLASK_APP=main.py

COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir 
RUN apk add --update --no-cache curl

COPY . .
CMD ["/bin/sh", "-c" , "/web/entrypoint.sh"] 
