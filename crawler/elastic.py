from elasticsearch import Elasticsearch
import base64

class ES(object):
    index = 'webpages'
    def __init__(self, host='localhost', port=9200):
        self.es = Elasticsearch([{
            'host':host,
            'port':9200
            }])

        self.create_index()


    def create_index(self):
        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(index=self.index, body={
                'settings': {
                    'analysis': {
                        'analyzer': {
                            'english_exact': {
                                'tokenizer': 'standard',
                                'filter': [
                                    'lowercase'
                                    ]
                                }
                            }
                        }
                    },
                'mappings': {
                    'properties': {
                        'content': {
                            'type': 'text',
                            'analyzer': 'english',
                            'fields': {
                                'exact': {
                                    'type': 'text',
                                    'analyzer': 'english_exact'
                                    }
                                }
                            }
                        }
                    }
                })

    def gen_id(self, url):
        url_bytes = url.encode('ascii')
        base64_bytes = base64.b64encode(url_bytes)
        base64_url = base64_bytes.decode('ascii')
        return base64_url


    def add_doc(self, title, url, content):
        self.es.index(index=self.index, doc_type='_doc', id=self.gen_id(url), body={
            'title': title,
            'url': url,
            'content': content
            })



    def search(self, query_string):
        response = self.es.search(index=self.index, doc_type='_doc', body={
            'query': {
                'simple_query_string': {
                    'fields': ['content'],
                    'quote_field_suffix': '.exact',
                    'query': query_string
                    }
                }
            })
        
        return response['hits']['hits']

