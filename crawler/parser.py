from bs4 import BeautifulSoup as bs
from bs4 import Comment
from urllib import parse
import re


class Parser(object):
    def __init__(self, base_url='iitd.ac.in', blacklist=['hospital.iitd.ac.in']):
        self.base_url = base_url
        self.blacklist = blacklist


    def parse_html(self, html):
        soup = bs(html, 'lxml')

        comments = soup.body.findAll(text=lambda t: isinstance(t, Comment)) if soup.body else []
        for comment in comments:
            comment.extract()

        for s in soup(['script', 'style']):
            s.extract()

        spec_char = re.compile(r'[^0-9a-zA-Z\s]')
        whitespace = re.compile(r'\s+')
 #       parsed = re.sub(spec_char, ' ', soup.body.text)
        parsed = re.sub(whitespace, ' ', soup.body.text) if soup.body else ''
        title = soup.title.string if soup.title else ''
        return title, parsed.lower()


    def extract_urls(self, html, root_url):
        soup = bs(html, 'lxml')
        links = soup.findAll('a')
#        print(links)
        urls = []
        for link in links:
            url = link.get('href')
 #           print(url)
            result, parsed_url = self.parse_url(url, root_url)
            
            if result:
                urls.append(parsed_url)

        return urls


    def parse_url(self, url, root_url):
        if not url:
            return False, None

        url = url[:-1] if url[-1] == '/' else url
        split_url = parse.urlsplit(url)
        

        if split_url.netloc in self.blacklist:
            return False, None


        if split_url.scheme and not 'http' in split_url.scheme:
            return False, None

        if not split_url.netloc:
            return True, parse.urljoin(root_url, split_url.path)
        
        if not self.base_url in split_url.netloc:
            return False, None

        return True, ''.join([split_url[0]+'://']+list(split_url[1:3]))
    
