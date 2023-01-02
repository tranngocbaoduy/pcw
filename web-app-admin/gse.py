
import requests
import uuid
import base64

from bs4 import BeautifulSoup
from typing import Optional, Sequence
from urllib.parse import urlencode, urlparse

class Response(object):

    def __init__(self, title, link, snippet, pagemap, **args):
        self.id = str(int(uuid.uuid4().hex[:6], base=16))
        self.title = title
        self.link = link
        self.snippet = snippet 
        self.pagemap = pagemap 
        self.domain = urlparse(link).netloc
        self.base_encoded_url = self.urlsafe_encode(link)
    
    def __str__(self):
        return f"{self.link} - {self.title}"
        
    def urlsafe_encode(self, url):
        return (
            base64.urlsafe_b64encode(url.encode("utf-8")).decode("utf-8").rstrip("=")
            if url
            else ""
        )

class HTMLObject(object):
    
    def __init__(self, url):
        self.url = url

    def get_content(self):
        r = requests.get(self.url)
        return r.text

class GoogleSearchEngine(object): 

    def __init__(self, allowed_site:str=""):
        # desktop user-agent
        self.USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        # mobile user-agent
        self.MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
        self.allowed_site = allowed_site 
        self.domain = urlparse(allowed_site).netloc
        self.site_name = self.domain.split('.')[0]

    def get_url_search(self, search_term:str="") -> str:
        params = {
            "q": f'{search_term} {self.site_name}', 
        }  
        return f"https://google.com/search?{urlencode(params)}"

    def get_search_results(self, url: str="") -> Sequence[str]:
        headers = {"user-agent": self.USER_AGENT}
        resp = requests.get(url, headers=headers)

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            results = self.extractor_url(soup)
            return results
        return []

    def extractor_url(self, soup) -> Sequence[str]:
        links = []
        for link in soup.findAll('a'):
            link = link.get('href')
            if link:
                domain = urlparse(link).netloc  
                if self.domain in link and link not in links:
                    links.append(link)
        links = list(sorted(links, key=lambda x: len(x)))
        return links[:3]


