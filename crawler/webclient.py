import requests
from urllib3 import disable_warnings


disable_warnings()


class WebClient(object):
    def __init__(self):
        self.session = requests.session()
        self.session.keep_alive = False


    def valid_response(self, resp):
        content = resp.headers.get('Content-Type')
        if content and 'text/html' in content and resp.status_code<400:
            return True

        return False


    def valid_url(self, url):
        resp = self.session.head(url, verify=False)
        return self.valid_response(resp), resp.url


    def get(self, url):
        return self.session.get(url, verify=False)
