import os
from bs4 import BeautifulSoup
import requests
import re
from pprint import pprint
from urllib.parse import urljoin
import logging
from collections import deque

logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')

class Crawler:
    def __init__(self, urls=[]):
        self.visited_urls = set()
        self.urls_to_visit = deque(urls)
        
    def download_url(self, url): return requests.get(url).text
    
    def bfs(self,url,html):
        soup = BeautifulSoup(html, 'html.parser')
        self.visited_urls.add(url)
        for link in soup.select("a[href$='.pdf']"):
            filename = os.path.join(os.getcwd(),link['href'].split('/')[-1])
            with open(filename, 'wb') as f:  f.write(requests.get(urljoin(url,link['href'])).content)
        
        for link in soup.find_all('a'):
            path = link.get('href')         
            if path: 
                if path.startswith('/'): 
                    if url.endswith('/'):  url = re.sub('/$', '', url)
                    path = url + path
                yield path
            
    
    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.popleft()
            if url not in self.visited_urls:
                logging.info('TRY: {}'.format(url))
                try: self.crawl(url)
                except Exception: logging.exception(f'Failed to crawl: {url}')
            
    def crawl(self,url):
        logging.info('Crawling: {}'.format(url))
        html = self.download_url(url) 
        for next_url in self.bfs(url, html):
            if next_url and next_url.startswith(url): self.urls_to_visit.append(next_url)
        
if __name__ == '__main__':
    #cw = Crawler(urls=['http://www.cnn.com/'])
    #cw.run()