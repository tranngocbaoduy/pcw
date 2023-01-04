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
from validators.url import url
from modules.crawler.models.sitemap import PageInfo, Sitemap 
from tools.scraper.scraper.utils import CrawlingHelper

class ScraperPipeline:
    
    def get_sitemap_item_db(self, spider): 
        try:
            if spider.spider.spider:
                return spider.spider.spider
        except:
            return spider.spider

    def get_params_from_raw(self, item, sitemap):
        list_meta = {}
        for meta in item.get('meta'):
            soup = BeautifulSoup(meta, 'html.parser')
            meta_attrs = [tag.attrs for tag in soup.findAll('meta')][0]
            attrs = ['og:image', 'og:title', 'og:description', 'keywords', 'description', 'og:keywords']
            if 'property' in meta_attrs.keys() and meta_attrs.get('property') in attrs:
                list_meta['property'] = meta_attrs.get('content')
            elif 'name' in meta_attrs.keys() and meta_attrs.get('name') in attrs:
                list_meta['name'] = meta_attrs.get('content')

        params = {
            "url": item.get('URL'),
            "title": '__'.join(item.get('title')),
            "encoded_base_url": item.get('encoded_base_url'),
            "meta": json.dumps(list_meta),
            "sitemap": sitemap
        } 
        return params

    def create_or_update_item(self, params):
        try:
            obj, created = PageInfo.objects.update_or_create(encoded_base_url=params.get('encoded_base_url'), defaults=params)
            if created:
                print({"message": "[CREATE PRODUCT]", "obj": obj})
            else:
                for key, value in params.items():
                    setattr(obj, key, value) 
                setattr(obj, 'count_update', obj.count_update + 1)  
                obj.save()
                print({"message": "[UPDATE PRODUCT]", "obj": obj})
            return params
        except Exception as e:
            print(e)
            return None

    def process_item(self, item, spider):
        sitemap = self.get_sitemap_item_db(spider) 
        params = self.get_params_from_raw(item, sitemap)
        retry_count = 0
        page_info = None
        while retry_count < 3 and page_info == None: 
            retry_count = retry_count + 1
            page_info = self.create_or_update_item(params)
        return page_info

    def close_spider(self, spider):
        print('[CLOSE SPIDER]', spider)
        pass
