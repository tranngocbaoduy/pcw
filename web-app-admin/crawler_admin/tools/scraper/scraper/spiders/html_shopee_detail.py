import scrapy
import logging
import scrapy
import json
import re
import time
import os
import sys
import base64

file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.abspath(file_dir + "/..")
sys.path.append(os.path.normpath(root_dir))
  
from lxml import etree 
from functools import reduce
from bs4 import BeautifulSoup
from django.utils import timezone
from urllib.parse import urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError, TimeoutError
from decimal import Decimal
from tools.scraper.scrapy_selenium import SeleniumRequest
from scrapy.utils.log import configure_logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from shutil import which

from tools.scraper.scraper.items import RawProductItem, ProductItem
from tools.scraper.scraper.utils import CrawlingHelper, MLStripper
from tools.scraper.scraper.proxy import ProxyService
from sys import platform

def get_driver():
    if platform == "linux" or platform == "linux2": # linux
        return which(os.path.join(root_dir, "geckodriver"))
    elif platform == "darwin": # OS X
        return which(os.path.join(root_dir, "geckodriver"))
    elif platform == "win32": # WIN
        return which(os.path.join(root_dir, "geckodriver.exe"))
    return which(os.path.join(root_dir, "geckodriver"))

def get_browser():
    if platform == "linux" or platform == "linux2": # linux
        return which('/Applications/Firefox.app/Contents/MacOS/firefox')
    elif platform == "darwin": # OS X
        return which('/Applications/Firefox.app/Contents/MacOS/firefox')
    elif platform == "win32": # WIN
        return which('C:\Program Files\Mozilla Firefox\firefox')
    return which('/Applications/Firefox.app/Contents/MacOS/firefox')

class HtmlShopeeDetailSpider(scrapy.Spider):
    # configure_logging(install_root_handler=False)
    # logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    name = "html_shopee_detail"
    start_request_time = None
    url_timeout = []
    custom_settings = {
        "DOWNLOAD_DELAY": 10,
        "SELENIUM_DRIVER_NAME": "firefox",
        "SELENIUM_DRIVER_EXECUTABLE_PATH": get_driver(),
        "SELENIUM_BROWSER_EXECUTABLE_PATH": get_browser(),
        "SELENIUM_DRIVER_ARGUMENTS": [],  # '--headless' if using chrome instead of firefox 
    }

    def __init__(self, *a, **kwargs): 
        super(HtmlShopeeDetailSpider, self).__init__(*a, **kwargs)
    
        self.spider = kwargs.get("spider")
        self.parsers = self.spider.parser_set.all()
        self.count_err = 0
        self.encoded_urls = []
        self.proxy_item = None
        self.retry = 0

        self.CLASS_PARENT = self.spider.class_parent
        self.CLASS_CHILD = self.spider.class_child
        self.START_URL = kwargs.get("url")
        self.LIMIT = int(self.spider.limit_per_request)
        self.FILE_PROXY_PATH = os.path.join(file_dir, "../proxy_list.json")
        self.IS_USING_PROXY = self.spider.is_using_proxy
        self.CURRENT_PAGE = int(self.spider.start_page)
        self.END_PAGE = int(self.spider.end_page)
        self.ALLOWED_DOMAINS = [self.spider.domain]
        self.BASE_URL_ITEM = self.spider.base_url_item
        self.IS_HEADLESS = self.spider.is_headless
        self.PARSER_WAIT_UNTIL_PARENT = self.spider.parser_wait_until_parent
        self.PARSER_WAIT_UNTIL_CHILD = self.spider.parser_wait_until_child

    def start_requests(self):
        yield self.get_new_request()

    def get_diff_time(self):
        if self.start_request_time == None:
            self.start_request_time = time.time()
            return 0
        else:
            diff = (time.time() - self.start_request_time) / 60
            self.start_request_time = time.time()
            return diff

    def get_new_request(self):
        url = self.START_URL
        params = {
            "url": url,
            "headers": {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.google.com/search?q=tiki&rlz=1C5CHFA_enVN972VN972&oq=tiki&aqs=chrome..69i57j0i67l4j69i60l3.1346j0j7&sourceid=chrome&ie=UTF-8",
            },
            "meta": {
                "max_retry_times": 1,
                "download_timeout": 20,
                "download_latency": 4,
            },
            "callback": self.parse_product_item,
            "errback": self.err_callback, 
            "dont_filter": True,
            "wait_time": 30,
            "wait_loaded": 4,
        }

        if not self.IS_HEADLESS:
            params["is_scroll_to_end_page"] = True
            tag = (self.PARSER_WAIT_UNTIL_CHILD.selector_type, self.PARSER_WAIT_UNTIL_CHILD.selector)
            params["wait_until"] = EC.visibility_of_element_located(tag)

        if self.IS_USING_PROXY:
            self.proxy_item = ProxyService.get_proxy_high_confident(
                self.FILE_PROXY_PATH, self.count_err
            )
            params["meta"]["proxy"] = self.proxy_item["curl"]
            CrawlingHelper.log(
                "=== Start request: {0} - {1} === ".format(url, self.proxy_item["curl"])
            )
        else:
            CrawlingHelper.log("=== Start request: {0} === ".format(url))
        self.start_urls.append(url)
        request = SeleniumRequest(**params)
        return request

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
        if self.IS_USING_PROXY:
            self.proxy_item = ProxyService.get_proxy_high_confident(
                self.FILE_PROXY_PATH, self.count_err
            )
            ProxyService.update_count_ip(
                self.FILE_PROXY_PATH, self.proxy_item.get("curl", ""), -100
            )
        yield self.get_new_request()

    def save_html(self, response, name):
        data_crawler_file_dir = "raw_html/{}".format(name)
        if not os.path.exists(data_crawler_file_dir):
            os.makedirs(data_crawler_file_dir)
        with open("{}/index.html".format(data_crawler_file_dir), "w") as f:
            f.write(response.text)
            f.close()
      
    def strip_tags(self, html):
        try:
            s = MLStripper()
            s.feed(html)
            return s.get_data()
        except:
            return html

    def get_basic_category(self, res_info):
        tree_category = res_info.get('itemListElement', [])
        list_category = []
        if tree_category and len(tree_category) != 0: 
            tree_category = sorted(tree_category, key=lambda x: x.get('position', 1), reverse=False)
            index = 0
            for category in tree_category: 
                if category.get('position') == 1: 
                    index += 1
                    continue
                item = category.get('item', None)
                if item == None: continue 
                params = {
                    "id": CrawlingHelper.urlsafe_encode(item.get('@id', '')),
                    "url": item.get('@id', ''),
                    "name": item.get('name', ''),
                }
                if index > 1 and index - 1 <= len(tree_category):
                    prev_item = tree_category[index - 1].get('item', None)
                    params['parent'] = prev_item.get('name', '')
                
                if index + 1 < len(tree_category):
                    next_item = tree_category[index + 1].get('item', None)
                    params['child'] = next_item.get('name', '')

                list_category.append(params)
                index += 1
        return list_category
        
    def get_basic_info(self, res_info):
        basic_info = {}
        basic_info['name'] = res_info.get('name', '')
        basic_info['description'] = res_info.get('description', '')
        basic_info['url'] = res_info.get('url', '')
        basic_info['image'] = res_info.get('image', '')
        basic_info['brand'] = res_info.get('brand', '')

        if res_info.get('offers'):
            basic_info['price'] = res_info['offers'].get('price', '')
            if basic_info['price'] == '':
                basic_info['price'] = res_info['offers'].get('lowPrice', '')
                basic_info['list_price'] = res_info['offers'].get('highPrice', '')
            else:
                basic_info['list_price'] = basic_info['price']
            
            if res_info['offers'].get('seller'):
                basic_info['seller'] = {
                    "name": res_info['offers']['seller'].get('name', ''),
                    "url": res_info['offers']['seller'].get('url', ''),
                    "image": res_info['offers']['seller'].get('image', ''), 
                }
                if res_info['offers']['seller'].get('aggregateRating'):
                    basic_info["seller"]["star"] = res_info['offers']['seller']['aggregateRating'].get('ratingValue', '')
                    basic_info["seller"]["review"] = res_info['offers']['seller']['aggregateRating'].get('ratingCount', '')
            
        if res_info.get('aggregateRating'):
            basic_info['star'] = res_info['aggregateRating'].get('ratingValue', '')
            basic_info['review'] = res_info['aggregateRating'].get('ratingCount', '')
            
        return basic_info

    def extract_tag_script_basic_info_shopee(self, html_page):
        soup = BeautifulSoup(html_page, "html.parser")
        dom = etree.HTML(str(soup))
        tag = dom.getiterator(tag='script')
        basic_info = {}
        for i in tag:
            if i.get('type') == 'application/ld+json':
                res_info = json.loads(i.text)
                if res_info.get('@type') == 'Product': 
                    basic_info.update(self.get_basic_info(res_info)) 
                if res_info.get("@type") == "BreadcrumbList":
                    tree_category = self.get_basic_category(res_info)
                    basic_info.update({
                        "tree_category": tree_category,
                        "category": tree_category[-2]
                    }) 
        # print('[basic_info] =>',basic_info)
        return basic_info

    def parse_product_item(self, response):
        base_url = os.path.dirname(response.request.url)

        merged_item = dict()
        merged_item["url"] = response.request.url
        merged_item["name"] = response.request.url.replace(base_url, "")
        merged_item["domain"] = self.spider.domain
        merged_item["agency"] = self.spider.agency
        merged_item["scraper_type"] = "html_shopee" 
        print("[URL]=>", merged_item["url"])
        basic_info = self.extract_tag_script_basic_info_shopee(response.text)

        info_from_parser = dict()
        for parser in self.parsers:

            # Get value from tag html
            if parser.name == "image" or parser.name == "img":
                # handle for image
                img_tags = self._parse_attribute(
                    response, parser.selector_type, parser.selector
                )
                list_url_images = self.handle_get_list_image(response, img_tags)
                info_from_parser["image"] = list_url_images
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
        self.save_html(response, merged_item["name"])
        merged_item.update(basic_info)
        merged_item.update(info_from_parser)
        print('[basic_info] =>', basic_info)

        if self.IS_USING_PROXY:
            ProxyService.update_count_ip(
                self.FILE_PROXY_PATH, self.proxy_item.get("curl", "")
            )
        return merged_item

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
        image_urls = CrawlingHelper.get_random_from_list(4, image_urls)
        return image_urls

    def _parse_attribute(self, dom, selector_type, selector):
        attribute = ""
        if selector_type == "xpath":
            attribute = dom.xpath(selector)
        if selector_type == "css":
            attribute = dom.css(selector)
        return attribute
