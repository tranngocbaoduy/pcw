# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import requests
import json
import datetime
import logging

from decimal import *
from bs4 import BeautifulSoup
from validators.url import url
from modules.crawler.models.sitemap import PageInfo, Sitemap 
from modules.crawler.models.product import Category, GroupProduct, Product, HistoryPricing
from tools.scraper.scraper.utils import CrawlingHelper
from pprint import pprint

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
        
        p1 = Decimal(item.get('price')) if item.get('price') and item.get('price') != '' else 0
        p2 = Decimal(item.get('list_price')) if item.get('list_price') and item.get('list_price') != '' else 0
        if not p2: p2 = p1
        if p1 and p1 > 0 and p2 and p2  > 0:
            if p1 > p2:
                p1, p2 = p2, p1
                discount_rate = 100 - int(Decimal(p1) / Decimal(p2) * 100)
            elif p1 * 2 < p2:
                p2 = p1
                discount_rate = 0 
            else:
                discount_rate = 100 - int(Decimal(p1) / Decimal(p2) * 100)

        params = { 
            "name": item.get('name','').strip(),
            "title": '__'.join(item.get('title',[''])),
            "base_url": item.get('URL'),
            "encoded_base_url": item.get('encoded_base_url'),
            "meta": json.dumps(list_meta),
            "description": "",
            "price": p1, 
            "list_price":p2,
            "list_image": json.dumps(item.get('list_image')),
            "category": item.get('category'),
            "discount_rate": discount_rate
        } 
        if params['name'] == None or params['name'] == '' or len(params['name']) > 512: params['name'] = params['title']
 
        return params

    def create_or_update_item(self, params, verbose=False):
        try:
            obj, created = PageInfo.objects.update_or_create(encoded_base_url=params.get('encoded_base_url'), defaults=params)
            if created:
                if verbose: print({"message": "[CREATE PAGE INFO]", "obj": obj})
            else:
                for key, value in params.items():
                    setattr(obj, key, value) 
                setattr(obj, 'count_update', obj.count_update + 1)  
                if verbose: print({"message": "[UPDATE PAGE INFO]", "obj": obj})
                obj.save()
            return params
        except Exception as e:
            print(e)
            return None
    
    def create_or_update_item_detail(self, params, verbose=False):
        try:
            obj, created = Product.objects.update_or_create(encoded_base_url=params.get('encoded_base_url'), defaults=params)
            if created:
                if verbose: print({"message": "[CREATE PRODUCT]", "obj": obj})
            else:
                for key, value in params.items():
                    setattr(obj, key, value) 
                setattr(obj, 'count_update', obj.count_update + 1)  
                if verbose: print({"message": "[UPDATE PRODUCT]", "obj": obj})
                obj.save()
            return obj
        except Exception as e:
            print(e)
            return None

    def create_or_update_history_pricing(self, product_info, params, verbose=False):
        if product_info.price != params.get('price') or product_info.list_price != params.get('list_price'):
            product_info.last_updated_price = (datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z')
            params = {
                "price": product_info.price,
                "list_price": product_info.list_price,
                "product": product_info,
            } 
            history_obj = HistoryPricing.objects.create(**params)
            if verbose: print({"message": "[CREATE HISTORY]", "obj": history_obj})
            product_info.save()

    def process_item(self, item, spider, verbose=True):
        sitemap = spider.sitemap 
        pprint(item)

        if spider.action == 'SITEMAP':
            params = self.get_params_from_raw(item, sitemap)
            retry_count = 0
            page_info = None
            while retry_count < 3 and page_info == None: 
                retry_count = retry_count + 1
                page_info = self.create_or_update_item(params, verbose)
            return page_info
        elif spider.action == 'UPDATE_DETAIL':
            params = self.get_params_from_raw_detail(item, sitemap) 
            page_info = PageInfo.objects.get(encoded_base_url=params['encoded_base_url']) 
            if params['name'] and params['price'] and params['list_price']:
                params['category'], is_created = Category.objects.get_or_create(name=item['category'])
                product_info = self.create_or_update_item_detail(params, verbose) 
                self.create_or_update_history_pricing(product_info, params, verbose)
                
                # Continue subscribe to product
                page_info.is_subscribe = True
                page_info.save()

                return product_info
            else:
                # Cancle subscribe to product
                page_info.is_subscribe = False
                page_info.save()
                # print('[{}]'.format(spider.action))
                # pprint(params)

        return None

    def close_spider(self, spider):
        sitemap = spider.sitemap  
        print('[CLOSE SPIDER]', spider, sitemap, spider.action)
        if spider.action == 'SITEMAP': sitemap.is_sitemap_running = False
        if spider.action == 'UPDATE_DETAIL': 
            sitemap.is_crawl_detail_running = False
            print("[UPDATE GROUP AND CATEGORIZE] ...")
            GroupProduct.update_all_info()
            Product.categorize_all()
            print("FINISHED UPDATING CATEGORIZATION !!")
        sitemap.save() 
        pass
