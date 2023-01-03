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
        self.encoded_urls = []  

        logging.getLogger('scrapy.utils.log').setLevel(logging.INFO)
        logging.getLogger('scrapy.extensions.telnet').setLevel(logging.WARNING)
        logging.getLogger('scrapy.middleware').setLevel(logging.WARNING)
        logging.getLogger('scrapy.core.scraper').setLevel(logging.INFO)

        self.base_url = self.spider.base_url
        self.total_page = 1 
        self.limit_page = 1 
        self.allowed_domains = [CrawlingHelper.get_domain(url=self.base_url)]  
        self.rule = Rule(
            LinkExtractor(
                allow=(self.allowed_domains), 
                tags=(),
                attrs=()
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

    def parse_pageinfo(self, response):
        clean_url = CrawlingHelper.get_clean_url(response.url)
        encoded_base_url = CrawlingHelper.urlsafe_encode(clean_url)
        if (response.headers.get('Content-Type')):
            content_type = response.headers['Content-Type'].decode('utf-8')
            if ('text/html' not in content_type):
                msg = "Not allow Content-Type: {}".format(content_type)
                logger.debug(msg)
                raise IgnoreRequest(msg)
        print('[CLEAN_URL]',clean_url)
        if clean_url and (not self.rule.link_extractor.matches(clean_url)):
            return None

        sel = Selector(response)
        item = PageInfoItem()
        item['URL'] = clean_url
        item['encoded_base_url'] = encoded_base_url
        item['title'] = sel.xpath('/html/head/title/text()').extract()
        item['meta'] = sel.xpath('/html/head/meta').getall() 

        # if ('iframe' in response.meta):
        new_links = LinkExtractor(allow=('^' + re.escape(self.base_url)), allow_domains=self.allowed_domains).extract_links(response)
        for link in new_links:
            if self.total_page < self.limit_page:
                self.total_page += 1
                print('[NEW_LINKS]', self.total_page, link.url)
                yield SeleniumRequest(
                    url=link.url, 
                    callback=self.parse_pageinfo,
                    errback=self.err_callback,)

        yield item
 
    # def get_new_request(self, url=None, is_child=False):
    #     url = url if url else self.START_URL.format(self.CURRENT_PAGE)
    #     params = {
    #         "url": url,
    #         "headers": {
    #             "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0",
    #             "X-Requested-With": "XMLHttpRequest",
    #             "Referer": "https://www.google.com/search?q=tiki&rlz=1C5CHFA_enVN972VN972&oq=tiki&aqs=chrome..69i57j0i67l4j69i60l3.1346j0j7&sourceid=chrome&ie=UTF-8",
    #         },
    #         "meta": {
    #             "max_retry_times": 2,
    #             "download_timeout": 20,
    #             "download_latency": 5,
    #         },
    #         "callback": self.parse_product_item if is_child else self.distribute_parse,
    #         "errback": self.err_callback,
    #         "dont_filter": True,
    #         "wait_time": 10,
    #         "wait_loaded": 10,
    #     }

    #     if not self.IS_HEADLESS and not is_child and self.PARSER_WAIT_UNTIL_PARENT and self.PARSER_WAIT_UNTIL_PARENT:
    #         params["is_scroll_to_end_page"] = True
    #         tag = (
    #             self.PARSER_WAIT_UNTIL_PARENT.selector_type,
    #             self.PARSER_WAIT_UNTIL_PARENT.selector,
    #         )
    #         params["wait_until"] = EC.presence_of_element_located(tag)

    #     if not self.IS_HEADLESS and is_child and self.PARSER_WAIT_UNTIL_PARENT and self.PARSER_WAIT_UNTIL_PARENT:
    #         params["is_scroll_to_end_page"] = True
    #         tag = (
    #             self.PARSER_WAIT_UNTIL_CHILD.selector_type,
    #             self.PARSER_WAIT_UNTIL_CHILD.selector,
    #         )
    #         params["wait_until"] = EC.visibility_of_element_located(tag)

    #     if self.IS_USING_PROXY:
    #         self.proxy_item = ProxyService.get_proxy_high_confident(
    #             self.FILE_PROXY_PATH, self.count_err
    #         )
    #         params["meta"]["proxy"] = self.proxy_item["curl"]
    #         CrawlingHelper.log(
    #             "=== Start request: {0} - {1} === ".format(url, self.proxy_item["curl"])
    #         )
    #     else:
    #         CrawlingHelper.log("=== Start request: {0} === ".format(url))
 
    #     self.start_urls.append(url)
    #     request = SeleniumRequest(**params)
    #     return request

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