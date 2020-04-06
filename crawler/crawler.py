from webclient import WebClient


class Crawler(object):
    def __init__(self, parser, es, urlbank):
        self.parser = parser
        self.es = es
        self.urlbank = urlbank
        self.webclient = WebClient()

    
    def crawl(self):
        while True:
            url = self.urlbank.next_task()

            try:
                resp = self.webclient.get(url)
            except Exception as e:
                print('\r'+__name__+': '+str(e)+': '+str(url))
                self.urlbank.task_done()
                continue

            urls = self.parser.extract_urls(resp.text, resp.url)
            self.urlbank.bulk_add_to_queue(urls)

            title, parsed_html = self.parser.parse_html(resp.text)
            self.es.add_doc(title, resp.url, parsed_html)
            self.urlbank.task_done()
