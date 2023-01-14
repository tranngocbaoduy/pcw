# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import requests
import json
import logging

from decimal import *
from bs4 import BeautifulSoup
from validators.url import url
from modules.crawler.models.sitemap import PageInfo, Sitemap 
from modules.crawler.models.product import Category, GroupProduct, Product 
from tools.scraper.scraper.utils import CrawlingHelper

class ScraperPipeline: 

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
    
    def get_params_from_raw_detail(self, item, sitemap):
        list_meta = {}
        for meta in item.get('meta'):
            soup = BeautifulSoup(meta, 'html.parser')
            meta_attrs = [tag.attrs for tag in soup.findAll('meta')][0]
            attrs = ['og:image', 'og:title', 'og:description', 'keywords', 'description', 'og:keywords']
            if 'property' in meta_attrs.keys() and meta_attrs.get('property') in attrs:
                list_meta['property'] = meta_attrs.get('content')
            elif 'name' in meta_attrs.keys() and meta_attrs.get('name') in attrs:
                list_meta['name'] = meta_attrs.get('content')

        discount_rate = 0 
        p1 = Decimal(item.get('price', 0))
        p2 = Decimal(item.get('list_price', 1))
        if p1 and p1 > 0 and p2 and p2  > 0:
            discount_rate = 100 - int(Decimal(p1) / Decimal(p2) * 100)

        params = { 
            "name": item.get('name').strip(),
            "title": '__'.join(item.get('title')),
            "base_url": item.get('URL'),
            "encoded_base_url": item.get('encoded_base_url'),
            "meta": json.dumps(list_meta),
            "description": "",
            "price": item.get('price'), 
            "list_price": item.get('list_price'),
            "list_image": json.dumps(item.get('list_image')),
            "category": item.get('category'),
            "discount_rate": discount_rate
        } 

        return params

    def create_or_update_item(self, params):
        try:
            obj, created = PageInfo.objects.update_or_create(encoded_base_url=params.get('encoded_base_url'), defaults=params)
            if created:
                print({"message": "[CREATE PAGE INFO]", "obj": obj})
            else:
                for key, value in params.items():
                    setattr(obj, key, value) 
                setattr(obj, 'count_update', obj.count_update + 1)  
                obj.save()
                print({"message": "[UPDATE PAGE INFO]", "obj": obj})
            return params
        except Exception as e:
            print(e)
            return None
    
    def create_or_update_item_detail(self, params):
        try:
            obj, created = Product.objects.update_or_create(encoded_base_url=params.get('encoded_base_url'), defaults=params)
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
        sitemap = spider.sitemap
        print('[{}]'.format(spider.action),item)
        if spider.action == 'SITEMAP':
            params = self.get_params_from_raw(item, sitemap)
            retry_count = 0
            page_info = None
            while retry_count < 3 and page_info == None: 
                retry_count = retry_count + 1
                page_info = self.create_or_update_item(params)
            return page_info
        elif spider.action == 'UPDATE_DETAIL':
            params = self.get_params_from_raw_detail(item, sitemap) 
            page_info = PageInfo.objects.get(encoded_base_url=params['encoded_base_url']) 
            if params['name'] and params['price'] and params['list_price']:
                params['category'], is_created = Category.objects.get_or_create(name=item['category'])
                product_info = self.create_or_update_item_detail(params) 
                
                # Continue subscribe to product
                page_info.is_subscribe = True
                page_info.save()

                return product_info
            
            # Cancle subscribe to product
            page_info.is_subscribe = False
            page_info.save()
            
        return None

    def close_spider(self, spider):
        sitemap = spider.sitemap  
        print('[CLOSE SPIDER]', spider, sitemap, spider.action)
        if spider.action == 'SITEMAP': sitemap.is_sitemap_running = False
        if spider.action == 'UPDATE_DETAIL': sitemap.is_crawl_detail_running = False
        sitemap.save() 
        pass
