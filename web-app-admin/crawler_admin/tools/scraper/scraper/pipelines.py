# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import requests
import json

from bs4 import BeautifulSoup
from django.utils import timezone
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from dateutil import parser
from validators.url import url
from modules.crawler.models import Item, News, RawProduct
from tools.scraper.scraper.utils import CrawlingHelper

class ScraperPipeline:
    def extract_text_item(self, item, scraper):
        def extract_text_with_bs4(attr):
            return BeautifulSoup(str(attr)).get_text().strip()

        if item['thumbnail_link']:
            thumbnail_link = BeautifulSoup(item['thumbnail_link'], 'html.parser')
            if thumbnail_link:
                thumbnail_link = thumbnail_link.img['src']
                if not(url(thumbnail_link)):
                    thumbnail_link = scraper.homepage + thumbnail_link
        else:
            thumbnail_link = None

        if item['image_link']:
            image_link = BeautifulSoup(item['image_link'], 'html.parser')
            if image_link:
                image_link = image_link.img['src']
                if not(url(image_link)):
                    image_link = scraper.homepage + image_link
        else:
            image_link = None

        output = {
            'title': extract_text_with_bs4(item['title']),
            'content': extract_text_with_bs4(item['content']),
            'author': extract_text_with_bs4(item['author']),
            'image_link': image_link,
            'thumbnail_link': thumbnail_link,
            # 'category': BeautifulSoup(item['category']).get_text(),
            # 'tag': BeautifulSoup(item['tag']).get_text(),
            'summary': extract_text_with_bs4(item['summary']),
            'published_at': parser.parse(' '.join(' '.join(extract_text_with_bs4(item['published_at']).split(' - ')).split(' | ')),
                                         fuzzy=True),
            'url': item['url']
        }
        return output 

    def convert_raw_product_db(self, item):
        return {
            "url": item.get('url'),
            "base_encoded_url": CrawlingHelper.urlsafre_encode(item.get('url')),
            "data": item,
        }

    def process_item(self, item, spider): 
        product = self.convert_raw_product_db(item)
        is_exist = True if len(RawProduct.objects.filter(base_encoded_url=product['base_encoded_url'])) != 0 else False
        if not is_exist:
            product, is_created = RawProduct.objects.get_or_create(**product)

        return product
