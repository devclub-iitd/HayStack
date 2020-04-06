from bs4 import BeautifulSoup as bs
from threading import Thread, current_thread, Lock
from collections import defaultdict
import requests
import urllib3
import atexit
from elastic import ES
from parser import Parser
from urlbank import UrlBank


lock = Lock()
crawled = 0
visited = 0
urllib3.disable_warnings()

PYTHONWARNINGS='ignore'
def valid_response(resp):
    headers = resp.headers
    content_type = headers.get('Content-Type')
#    print(resp.status_code)
    if resp.status_code<400 and 'text/html' in content_type:
        return True
    return False


def crawl(parser, urlbank, es):
    global visited, crawled

    s = requests.session()
    s.keep_alive = False
    wait = ['|','/','-','\\']
    counter = 0

    while True:
     #   print('\r'+wait[counter], end='')
        counter = (counter+1)%4
        url = urlbank.que.get()
        if urlbank.has_visited(url):
            urlbank.que.task_done()
            continue
        try:
            resp = s.head(url, verify=False, timeout=(5,30))
            urlbank.add_visited(resp.url)
            lock.acquire()
            visited += 1
            lock.release()
 #           print(valid_response(resp))
            if valid_response(resp) and not urlbank.has_crawled(resp.url): 
                urlbank.add_crawled(resp.url)
                lock.acquire()
                crawled += 1
                lock.release()
 #               print(current_thread().name + ': ' +  url)
                resp = s.get(url, verify=False)
     #           print(resp.url)
                urls = parser.extract_urls(resp.content, resp.url)
                urlbank.bulk_add_to_queue(urls)
     #           print(urls)
                
                parsed_html = parser.parse_html(resp.content)
                es.add_doc(resp.url, parsed_html)
            
        except requests.exceptions.ConnectionError:
             print('\rConnection Error: ' +url)
        except requests.exceptions.MissingSchema:
            print('\rInvalid schema: ' + url)
        except requests.exceptions.ReadTimeout:
            print('\rConnection Error: '+ url)
        except Exception as e:
            print('\r'+str(e))
            print(url)
        urlbank.que.task_done()
        #x = input()
        print('\r'+str(visited)+' '+str(crawled), end='')
    #print('\r')

def take_query(es):
    while True:
        q = input('Enter query string: ')
        results = es.search(q)
   
        for i in range(min(len(results),3)):
            r = results[i]
            print(r['_score'], r['_source']['url'])


def main():
    es = ES()
    parser = Parser('iitd.ac.in',['hospital.iitd.ac.in'])
    urlbank = UrlBank(['http://caic.iitd.ac.in/','http://bsw.iitd.ac.in', 'http://brca.iitd.ac.in', 'http://sac.iitd.ac.in'])
    
    atexit.register(urlbank.exit_routine)

    for i in range(8):
        crawler = Thread(target=crawl, daemon=True, name='Crawler '+str(i), args=(parser, urlbank, es))
        crawler.start()

    urlbank.que.join()
    print('\n')
    #print(len(urlbank.crawled.keys()))
    #print(urlbank.crawled['http://bsw.iitd.ac.in/'])
    
    #take_query(es)


if __name__=='__main__':
    main()
