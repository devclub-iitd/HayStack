FROM python:3.9.1-buster

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y netcat

# Copy requirements first so these layers can be cached
COPY requirements.txt /code

RUN pip install -r requirements.txt --prefer-binary

COPY ./crawling__iitd .

CMD scrapy crawl IITD --nolog


# RUN chmod +x /code/entry-point.sh
# ENTRYPOINT [ "/code/entry-point.sh" ]