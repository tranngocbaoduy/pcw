# -*- coding: utf-8 -*-
import scrapy
import logging
import scrapy
import json
import re
import time
import os
import sys

file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(file_dir + "/..")
sys.path.append(os.path.normpath(root_dir))

from urllib.parse import urlparse    
from scrapy.linkextractors import LinkExtractor

from pprint import pprint
from ..items import PageInfoItem
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders.crawl import Rule

from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.exceptions import IgnoreRequest
from twisted.internet.error import DNSLookupError, TCPTimedOutError, TimeoutError 
from shutil import which 
from tools.scraper.scraper.utils import CrawlingHelper
from tools.scraper.scraper.proxy import ProxyService
from sys import platform
from tools.scraper.scrapy_selenium import SeleniumRequest 
import requests
from bs4 import BeautifulSoup
 

def extract_links_by_bs(html, list_deny, main_url): 
    soup = BeautifulSoup(html, 'html.parser') 
    tag_a_links = [link.get('href') for link in soup.find_all('a')] 
    scripts = soup.find_all('script')
    tag_script_links = [link['src'] for link in scripts if 'src' in link.attrs]
    urls = [ url for url in list(set(tag_a_links + tag_script_links)) if url and url not in list_deny]
    final_url = []
    for url in urls: 
        if main_url not in url: final_url.append(main_url + url)
        else: final_url.append(url)
    return final_url

class HtmlHeadless(scrapy.Spider): 
    name = "html_headless"
    start_request_time = None
    url_timeout = []
    if platform == 'win32':
        import configparser
        import os

        mozilla_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox')
        mozilla_profile_ini = os.path.join(mozilla_profile, r'profiles.ini')
        profile = configparser.ConfigParser()
        profile.read(mozilla_profile_ini)
        data_path = os.path.normpath(os.path.join(mozilla_profile, profile.get('Profile0', 'Path')))


    custom_settings = {
        "DOWNLOAD_DELAY": 10,
        "SELENIUM_DRIVER_NAME": "chrome",
        "SELENIUM_DRIVER_EXECUTABLE_PATH": which(os.path.join(root_dir, "geckodriver"))
        if platform == "win32"
        else which(os.path.join(root_dir, "geckodriver.exe")),
        "SELENIUM_BROWSER_EXECUTABLE_PATH": which(os.path.join(root_dir, "chromedriver.exe"))
        if platform == "win32"
        else which("/Applications/Firefox.app/Contents/MacOS/firefox"),
        "SELENIUM_DRIVER_ARGUMENTS": [
            "--headless", 
            "--no-sandbox",
            "--disable-gpu", 
            # "--disable-dev-shm-usage"
        ],  # '--headless' if using chrome instead of firefox
        'DOWNLOADER_CLIENTCONTEXTFACTORY': 'crawler_admin.contextfactory.LegacyConnectContextFactory', 
    }

    # custom_settings = {
    #     "DOWNLOAD_DELAY": 10,
    #     "SELENIUM_DRIVER_NAME": "firefox",
    #     "SELENIUM_DRIVER_EXECUTABLE_PATH": which(
    #         os.path.join(root_dir, "geckodriver")
    #     )
    #     if platform == "win32"
    #     else which(os.path.join(root_dir, "geckodriver")),
    #     "SELENIUM_BROWSER_EXECUTABLE_PATH": which(r"C:\Program Files\Mozilla Firefox\firefox.exe" )
    #     if platform == "win32"
    #     else which("/Applications/Firefox.app/Contents/MacOS/firefox"),
    #     "SELENIUM_DRIVER_ARGUMENTS": [
    #         "--headless"
    #     ],  # '--headless' if using chrome instead of firefox
    #     'DOWNLOADER_CLIENTCONTEXTFACTORY': 'crawler_admin.contextfactory.LegacyConnectContextFactory', 

    # }

    def __init__(self, *a, **kwargs):
        super(HtmlHeadless, self).__init__(*a, **kwargs)

        self.sitemap = kwargs.get("sitemap")
        self.count_err = 0
        self.count_candidates = 0

        logging.getLogger('scrapy.utils.log').setLevel(logging.INFO)
        logging.getLogger('scrapy.extensions.telnet').setLevel(logging.WARNING)
        logging.getLogger('scrapy.middleware').setLevel(logging.WARNING)
        logging.getLogger('scrapy.core.scraper').setLevel(logging.INFO)

        self.base_url = CrawlingHelper.get_url_formatted(self.sitemap.base_url)
        self.main_url = CrawlingHelper.get_main_url(self.sitemap.base_url)
        self.encoded_base_url = CrawlingHelper.urlsafe_encode(self.base_url)
        self.encoded_urls = [self.encoded_base_url]  
        self.list_target_search_terms = self.sitemap.target_search_terms.split(',')
        self.list_exclude_search_terms = self.sitemap.exclude_search_terms.split(',')
        self.action = 'SITEMAP'

        self.count_pages = 1 
        self.limit_page = int(self.sitemap.limit_page)
        self.allowed_domains = [CrawlingHelper.get_domain(url=self.base_url)]
        self.rule = Rule(
            LinkExtractor(
                allow=(self.allowed_domains), 
            ),
            callback='parse_pageinfo',
            follow=True
        ) 
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
            "Accept-Encoding": "gzip, deflate, br", 
            "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,ja;q=0.4", 
            "Sec-Fetch-Dest": "document",
            "Referer": "https://www.google.com/",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1", 
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.127 Safari/537.36",
        }
        self.list_deny = []
        print('custom_settings', self.custom_settings)
        print({
            'platform': platform,
            'base_url': self.base_url,
            'limit_page': self.limit_page,
            'allowed_domains': self.allowed_domains
        })

    def start_requests(self):
        
        if self.count_err < 3:
            yield SeleniumRequest(
                url=self.base_url, 
                callback=self.parse_pageinfo,
                errback=self.err_callback,
                headers=self.headers
            )
            
    def is_candidate(self, url): 
        for i in self.list_exclude_search_terms:
            if i in url:
                return False
        for i in self.list_target_search_terms:
            if i in url:
                return True 
        return False

    def parse_pageinfo(self, response):
        clean_url = CrawlingHelper.get_clean_url(response.url)
        encoded_base_url = CrawlingHelper.urlsafe_encode(clean_url)
        if (response.headers.get('Content-Type')):
            content_type = response.headers['Content-Type'].decode('utf-8')
            if ('text/html' not in content_type):
                msg = "Not allow Content-Type: {}".format(content_type)
                logger.debug(msg)
                raise IgnoreRequest(msg)
        if clean_url and (not self.rule.link_extractor.matches(clean_url)):
            return None

        new_links = [tlink.url for tlink in LinkExtractor(
            allow_domains=self.allowed_domains,
            deny=self.list_deny).extract_links(response)]

        new_links_bs = extract_links_by_bs(response.text, self.list_deny, self.main_url)
        pprint(new_links_bs)
        new_links = list(set(new_links + new_links_bs))
        pprint({
            "link": clean_url,
            "new_links": len(new_links), 
            "new_links_bs": len(new_links_bs),
        })
        for link in new_links:
            try:
                new_url = CrawlingHelper.get_clean_url(link) 
                if self.is_candidate(new_url):  
                    encoded_new_url = CrawlingHelper.urlsafe_encode(new_url)
                    if self.count_pages < self.limit_page and encoded_new_url not in self.encoded_urls:
                        self.encoded_urls.append(encoded_new_url) 
                        self.list_deny.append(link)
                        self.count_pages += 1
                        print(' => [🌚🌚🌚 NEW_LINKS - {}]'.format(self.count_pages), new_url)
                        yield SeleniumRequest(
                            url=new_url, 
                            callback=self.parse_pageinfo,
                            errback=self.err_callback,
                            headers=self.headers,
                        ) 
                    else:
                        if link not in self.list_deny:
                            self.list_deny.append(link)
                else:
                    if link not in self.list_deny:
                        self.list_deny.append(link)
            except Exception as e:
                print('Error link:', link)

        if self.is_candidate(clean_url):
            self.save_html(response, encoded_base_url)
                
            sel = Selector(response)
            item = PageInfoItem()
            item['URL'] = clean_url
            item['encoded_base_url'] = encoded_base_url
            item['title'] = sel.xpath('/html/head/title/text()').extract()
            item['meta'] = sel.xpath('/html/head/meta').getall()  
    
            self.count_candidates+=1
            print(' => [🔥🔥🔥 CANDIDATE_URL - {}]'.format(str(self.count_candidates)),clean_url)
            yield item
  
    def err_callback(self, failure):
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            print("HttpError on %s", response)
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.url_timeout.append(request.url)
            print("DNSLookupError on %s", request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.url_timeout.append(request.url)
            print("TimeoutError on %s", request.url)
        else:
            print("Failure Undefined", failure)
        self.count_err += 1
        # if self.IS_USING_PROXY:
        #     self.proxy_item = ProxyService.get_proxy_high_confident(
        #         self.FILE_PROXY_PATH, self.count_err
        #     )
        #     ProxyService.update_count_ip(
        #         self.FILE_PROXY_PATH, self.proxy_item.get("curl", ""), -100
        #     )
        # yield self.start_requests()

    def save_html(self, response, name):
        data_crawler_file_dir = "raw_html/{}".format(name.replace(' ','_'))
        if not os.path.exists(data_crawler_file_dir):
            os.makedirs(data_crawler_file_dir)
        with open("{}/index.html".format(data_crawler_file_dir), "w",encoding='utf-8') as f:
            f.write(response.text)
            f.close() 