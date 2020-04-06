from threading import Thread, current_thread, Lock
import atexit
from elastic import ES
from parser import Parser
from urlbank import UrlBank
from crawler import Crawler


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
    urlbank = UrlBank(['http://caic.iitd.ac.in', 'http://bsw.iitd.ac.in', 'http://sac.iitd.ac.in', 'http://brca.iitd.ac.in', 'http://smp.iitd.ac.in', 'https://ngu.iitd.ac.in','https://webmail.iitd.ac.in','http://iitd.ac.in'])
    
    atexit.register(urlbank.exit_routine)

    crawlers = []
    for i in range(8):
        crawler = Crawler(parser, es, urlbank)
        crawlers.append(crawler)
        thread = Thread(target=crawler.crawl, daemon=True, name='Crawler '+str(i))
        thread.start()

    urlbank.que.join()
    print('\n')
    #print(len(urlbank.crawled.keys()))
    #print(urlbank.crawled['http://bsw.iitd.ac.in/'])
    
    #take_query(es)


if __name__=='__main__':
    main()
