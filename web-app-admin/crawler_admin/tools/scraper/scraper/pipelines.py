# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import requests
import json
import logging

from bs4 import BeautifulSoup
from django.utils import timezone
from django.forms.models import model_to_dict
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from dateutil import parser
from validators.url import url
from tools.scraper.scraper.utils import CrawlingHelper


class ScraperPipeline:
    
    def process_item(self, item, spider):
        print('[PROCESS ITEM]',item)
        return item

    def close_spider(self, spider):
        print('[CLOSE SPIDER]', spider)
        pass
