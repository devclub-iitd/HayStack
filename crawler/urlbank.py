from collections import defaultdict
from queue import Queue

class EmptyStartListException(Exception):
    def __init__(self, message):
        self.message = message


class DefaultdictQueue(Queue):
    def __init__(self, *args, **kwargs):
        super(DefaultdictQueue, self).__init__(*args, **kwargs)
        self.queue = defaultdict(bool)

    def _put(self, item):
        self.queue[item] = True

    def _get(self):
        key = list(self.queue.keys())[0]
        del(self.queue[key])
        return key

    def __contains__(self, item):
        return bool(self.queue.get(item))

    
class UrlBank(object):
    def __init__(self, start_list):
        self.crawled = defaultdict(bool)
        self.visited = defaultdict(bool)
        self.que = DefaultdictQueue()

        self.init_queue(start_list)
        self.init_crawled()
        self.init_visited()


    def init_queue(self, start_list):
        if start_list == []:
            raise EmptyStartListException('No urls in start list')
        else:
            for url in start_list:
                self.que.put(url)

        with open('queue.txt', 'r') as q:
            lines = q.read().split()
            for url in lines:
                self.que.put(url)

    
    def init_crawled(self):
        with open('crawled.txt', 'r') as c:
            lines = c.read().split()
            for url in lines:
                self.crawled[url] = True


    def init_visited(self):
        with open('visited.txt', 'r') as v:
            lines = v.read().split()
            for url in lines:
                self.visited[url] = True


    def next(self):
        return self.que.get()


    def add_to_queue(self, url):
        if not url in self.que:
            self.que.put(url)


    def bulk_add_to_queue(self, urls):
        for url in urls:
            self.add_to_queue(url)


    def has_crawled(self, url):
        return bool(self.crawled.get(url))


    def add_crawled(self, url):
        self.crawled[url] = True


    def has_visited(self, url):
        return bool(self.crawled.get(url))


    def add_visited(self, url):
        self.visited[url] = True


    def exit_routine(self):
        with open('queue.txt', 'w+') as q:
            q.write('\n'.join(list(self.que.queue)))
            q.close()

        with open('crawled.txt', 'w+') as c:
            c.write('\n'.join(list(self.crawled.keys())))
            c.close()

        with open('visited.txt', 'w+') as v:
            v.write('\n'.join(list(self.visited.keys())))
            v.close()
