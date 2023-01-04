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

from ..items import PageInfoItem
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders.crawl import Rule

from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.exceptions import IgnoreRequest
from twisted.internet.error import DNSLookupError, TCPTimedOutError, TimeoutError
from tools.scraper.scrapy_selenium import SeleniumRequest 
from shutil import which 
from tools.scraper.scraper.utils import CrawlingHelper
from tools.scraper.scraper.proxy import ProxyService
from sys import platform


class HtmlHeadless(scrapy.Spider): 
    name = "html_headless"
    start_request_time = None
    url_timeout = []

    custom_settings = {
        "DOWNLOAD_DELAY": 10,
        "SELENIUM_DRIVER_NAME": "firefox",
        "SELENIUM_DRIVER_EXECUTABLE_PATH": which(
            os.path.join(root_dir, "geckodriver.exe")
        )
        if platform == "win32"
        else which(os.path.join(root_dir, "geckodriver")),
        "SELENIUM_BROWSER_EXECUTABLE_PATH": which(
            "C:\Program Files\Mozilla Firefox\firefox"
        )
        if platform == "win32"
        else which("/Applications/Firefox.app/Contents/MacOS/firefox"),
        "SELENIUM_DRIVER_ARGUMENTS": [
            "--headless"
        ],  # '--headless' if using chrome instead of firefox
    }

    def __init__(self, *a, **kwargs):
        super(HtmlHeadless, self).__init__(*a, **kwargs)

        self.spider = kwargs.get("spider")
        self.count_err = 0
        self.count_candidates = 0

        logging.getLogger('scrapy.utils.log').setLevel(logging.INFO)
        logging.getLogger('scrapy.extensions.telnet').setLevel(logging.WARNING)
        logging.getLogger('scrapy.middleware').setLevel(logging.WARNING)
        logging.getLogger('scrapy.core.scraper').setLevel(logging.INFO)

        self.base_url = CrawlingHelper.get_url_formatted(self.spider.base_url)
        self.encoded_base_url = CrawlingHelper.urlsafe_encode(self.base_url)
        self.encoded_urls = [self.encoded_base_url]  
        self.list_target_search_terms = self.spider.target_search_terms.split(',')
        self.list_exclude_search_terms = self.spider.exclude_search_terms.split(',')

        self.count_pages = 1 
        self.limit_page = int(self.spider.limit_page)
        self.allowed_domains = [CrawlingHelper.get_domain(url=self.base_url)]
        self.rule = Rule(
            LinkExtractor(
                allow=(self.allowed_domains)
            ),
            callback='parse_pageinfo',
            follow=True
        ) 
        print('custom_settings', self.custom_settings)
        print({
            'base_url': self.base_url,
            'limit_page': self.limit_page,
            'allowed_domains': self.allowed_domains
        })

    def start_requests(self):
        if self.count_err < 3:
            yield SeleniumRequest(
                url=self.base_url, 
                callback=self.parse_pageinfo,
                errback=self.err_callback,)
            
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

        sel = Selector(response)
        item = PageInfoItem()
        item['URL'] = clean_url
        item['encoded_base_url'] = encoded_base_url
        item['title'] = sel.xpath('/html/head/title/text()').extract()
        item['meta'] = sel.xpath('/html/head/meta').getall() 

        new_links = LinkExtractor(allow=('^' + re.escape(self.base_url)), allow_domains=self.allowed_domains).extract_links(response)
        for link in new_links:
            new_url = CrawlingHelper.get_clean_url(link.url)
            if self.is_candidate(new_url):
                encoded_new_url = CrawlingHelper.urlsafe_encode(new_url)
                if self.count_pages < self.limit_page and encoded_new_url not in self.encoded_urls:
                    self.encoded_urls.append(encoded_new_url)
                    self.count_pages += 1
                    print(' => [🌚🌚🌚 NEW_LINKS - {}]'.format(self.count_pages), new_url)
                    yield SeleniumRequest(
                        url=new_url, 
                        callback=self.parse_pageinfo,
                        errback=self.err_callback,)
        if self.is_candidate(clean_url):
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
        yield self.start_requests()

    def save_html(self, response, name):
        data_crawler_file_dir = "raw_html/{}".format(name)
        if not os.path.exists(data_crawler_file_dir):
            os.makedirs(data_crawler_file_dir)
        with open("{}/index.html".format(data_crawler_file_dir), "w") as f:
            f.write(response.text)
            f.close() 