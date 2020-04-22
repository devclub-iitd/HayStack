from collections import defaultdict
from queue import Queue
from webclient import WebClient


class EmptyStartListException(Exception):
    def __init__(self, message):
        self.message = message

    
class UrlBank(object):
    def __init__(self, start_list):
        self.processed = defaultdict(bool)
        self.que = Queue()
        self.failed = []
        self.webclient = WebClient()
        self.nque = 0
        self.ndone = 0
        self.nproc = 0

        self.init_processed()
        self.init_queue(start_list)
        self.init_failed()


    def init_queue(self, start_list):
        if start_list == []:
            raise EmptyStartListException('No urls in start list')
        else:
            self.bulk_add_to_queue(start_list)

        with open('queue.txt', 'r') as q:
            lines = q.read().split()
            self.bulk_add_to_queue(lines)
            q.close()

    
    def init_processed(self):
        with open('processed.txt', 'r') as p:
            lines = p.read().split()
            for url in lines:
                self.processed[url] = True
            p.close()


    def init_failed(self):
        with open('failed.txt', 'r') as f:
            lines = f.read().split()
            for url in lines:
                self.failed.append(url)
            f.close()

    
    def update(self):
        #print(str(self.nproc)+' '+str(self.nque)+' '+str(self.ndone), end='              \r', flush=True)
       pass 

    def next_task(self):
        return self.que.get()


    def add_to_queue(self, url):
        if not self.has_processed(url):
            self.add_to_processed(url)
            try:
                valid, url = self.webclient.valid_url(url)
                self.add_to_processed(url)
                if valid:
                    self.que.put(url)
                    self.nque += 1
            except Exception as e:
                self.add_to_failed(url)
#                print('\r'+__file__+': '+str(e)+': '+str(url))
            self.update()

    def bulk_add_to_queue(self, urls):
        for url in urls:
            self.add_to_queue(url)


    def has_processed(self, url):
        return bool(self.processed.get(url))


    def add_to_processed(self, url):
        if not self.has_processed(url):
            self.nproc += 1
            self.processed[url] = True


    def add_to_failed(self, url):
        self.failed.append(url)


    def task_done(self):
        self.que.task_done()
        self.nque -= 1
        self.ndone += 1
        self.update()

    def exit_routine(self):
        with open('queue.txt', 'w+') as q:
            q.write('\n'.join(list(self.que.queue)))
            q.close()

        with open('processed.txt', 'w+') as p:
            p.write('\n'.join(list(self.processed.keys())))
            p.close()
        
        with open('failed.txt', 'w+') as f:
            f.write('\n'.join(self.failed))
            f.close()

