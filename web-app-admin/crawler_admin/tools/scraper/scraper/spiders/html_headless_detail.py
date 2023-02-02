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
from ..items import ProductInfoItem
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders.crawl import Rule

from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.exceptions import IgnoreRequest
from twisted.internet.error import DNSLookupError, TCPTimedOutError, TimeoutError
from tools.scraper.scrapy_selenium import SeleniumRequest 
from shutil import which 
from tools.scraper.scraper.utils import CrawlingHelper, MLStripper
from tools.scraper.scraper.proxy import ProxyService
from sys import platform

from modules.crawler.models.parser import Parser

class HtmlHeadlessDetail(scrapy.Spider): 
    name = "html_headless_detail"
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
        super(HtmlHeadlessDetail, self).__init__(*a, **kwargs)

        self.sitemap = kwargs.get("sitemap")
        self.page_info_items = kwargs.get("page_info_items")
        self.count_err = 0
        self.count_candidates = 0

        logging.getLogger('scrapy.utils.log').setLevel(logging.INFO)
        logging.getLogger('scrapy.extensions.telnet').setLevel(logging.WARNING)
        logging.getLogger('scrapy.middleware').setLevel(logging.WARNING)
        logging.getLogger('scrapy.core.scraper').setLevel(logging.INFO)

        self.base_url = self.sitemap.base_url
        self.category_name = self.sitemap.category_name
        self.encoded_base_url = CrawlingHelper.urlsafe_encode(self.base_url)
        self.encoded_urls = [self.encoded_base_url]        
        self.parsers = Parser.objects.filter(ware_parser=self.sitemap.ware_parser.id)
        self.action = 'UPDATE_DETAIL'
          
        pprint({
            "custom_settings": self.custom_settings,
            'base_url': self.base_url, 
            "parsers": self.parsers,
            "page_info_items": self.page_info_items
        })

    def start_requests(self):
        for sub_page in self.page_info_items:
            yield SeleniumRequest(
                url=sub_page.url, 
                callback=self.parse_product_item,
                errback=self.err_callback,
                wait_loaded=10
            )

    def parse_product_item(self, response):
        clean_url = CrawlingHelper.get_clean_url(response.url)
        encoded_base_url = CrawlingHelper.urlsafe_encode(clean_url)

        sel = Selector(response)
        item = ProductInfoItem()
        item['URL'] = clean_url
        item['encoded_base_url'] = encoded_base_url
        item['title'] = sel.xpath('/html/head/title/text()').extract()
        item['meta'] = sel.xpath('/html/head/meta').getall() 
        item['category'] = self.category_name 

        self.save_html(response, item['title'])
        info_from_parser = dict()
        for parser in self.parsers:

            # Get value from tag html
            if parser.name in ['list_image', 'images', 'img']:
                # handle for image
                img_tags = self._parse_attribute(
                    response, parser.selector_type, parser.selector
                ) 
                list_url_images = self.handle_get_list_image(response, img_tags)
                info_from_parser["list_image"] = list_url_images if list_url_images else []
            else:
                tags = self._parse_attribute(
                    response, parser.selector_type, parser.selector
                ).getall()
                str_tags = " ".join([self.strip_tags(html) for html in tags if html]) 
                if str_tags:
                    if "price" in parser.name:
                        # handle for currency
                        info_from_parser[
                            parser.name
                        ] = CrawlingHelper.get_currency_from_text(str_tags)
                    else:
                        # handle for value of parser
                        info_from_parser[parser.name] = str_tags
                else:
                    info_from_parser[parser.name] = ""     
        for key, value in info_from_parser.items():
            if key in item.fields.keys():
                item[key] = value 
        return item
 
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

    def strip_tags(self, html):
        try:
            s = MLStripper()
            s.feed(html)
            return s.get_data()
        except:
            return html

    def handle_get_list_image(self, dom, selector_items):
        image_urls = [] 
        for selector in selector_items:
            try:
                image_element_items = selector.css("img").xpath("@src").getall()
                for img_element in image_element_items:
                    if "https://" in img_element: 
                        image_urls.append(img_element)
            except:
                print("not image")
        image_urls = list(set(image_urls))
        # image_urls = CrawlingHelper.get_random_from_list(4, image_urls)
        return image_urls[:4]

    def _parse_attribute(self, dom, selector_type, selector):
        attribute = ""
        if selector_type == "xpath":
            attribute = dom.xpath(selector)
        if selector_type == "css":
            attribute = dom.css(selector)
        return attribute

    def save_html(self, response, name):
        data_crawler_file_dir = "raw_html/{}".format(name)
        if not os.path.exists(data_crawler_file_dir):
            os.makedirs(data_crawler_file_dir)
        with open("{}/index.html".format(data_crawler_file_dir), "w") as f:
            f.write(response.text)
            f.close() 