import json
import logging
from apscheduler.jobstores.base import JobLookupError
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from scrapy.settings import Settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from modules.crawler.apps import scheduler
from tools.scraper.scraper.spiders.news import NewsSpider
from tools.scraper.scraper.spiders.tiki import TikiSpider
from modules.crawler.handlers.extractor import ExtractorService

# Create your models here.
class Spider(models.Model):
    name = models.CharField(max_length=256)
    url = models.CharField('URL', max_length=512)
    domain = models.CharField('domain', default='',max_length=256)
    is_multiple = models.BooleanField('Multiple')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def group_product_by_code(self):
        list_product = Product.objects.filter(category=self.id)
        list_product_code = [ product.product_code for product in list_product]
        stat = self.handle_stat_group(list_product_code)
        for name, quantity in stat.items():
            info_group_product = {
                "category": self,
                "name": name,
                "quantity": quantity,
            }
            info_group_product, created = GroupProduct.objects.get_or_create(**info_group_product)
            if not created:
                # print({"message":'[UPDATE BRAND]', "info_brand": model_to_dict(info_brand)})
                for attr, value in model_to_dict(info_brand).items():
                    if attr == 'category': setattr(info_brand, attr, self)
                    else: setattr(info_brand, attr, value)
                info_brand.save()
        print("[GROUP {} PRODUCT ITEMS]".format(len(list_product)),stat)


    def handle_stat_group(self, texts):
        stat_group = {}
        for i in texts:
            if i not in stat_group:
                stat_group[i] = 1
            else:
                stat_group[i] +=1
        return stat_group 

class Brand(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.name, self.category.name)

class Shop(models.Model):
    name = models.CharField(max_length=256, blank=True)
    address = models.CharField(max_length=256, blank=True)
    agency = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.name, self.agency)

class GroupProduct(models.Model):
    name = models.CharField(max_length=50, blank=True)
    quantity = models.CharField(max_length=50, blank=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    agencies = ArrayField(
        ArrayField(
            models.CharField(max_length=10, blank=True),
            size=10,
            blank=True,
        ),
        size=100,
        default=list
    )
    product_ids = ArrayField(
        ArrayField(
            models.CharField(max_length=10, blank=True),
            size=8,
            blank=True,
        ),
        size=1000,
        default=list
    )
 
    def __str__(self):
        return '{} - {}'.format(self.name, str(self.quantity))

class Product(models.Model): 
    name = models.CharField('Name', max_length=256)
    clean_name = models.CharField('Clean Name', max_length=256)
    url = models.CharField('URL', max_length=512)
    base_encoded_url = models.CharField('Encode URL', max_length=512)
    domain = models.CharField('Domain', max_length=256)
    agency = models.CharField('Agency', max_length=256)
    product_code = models.CharField('Code', max_length=256)
    is_api = models.BooleanField('From API', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    group_product = models.ForeignKey(GroupProduct, blank=True, null=True, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    slug_id = models.TextField(default='', blank=True,)
    image = models.TextField(default='', blank=True,)
    shop = models.TextField(default='', blank=True,null=True)
    item_rating = models.TextField(default='', blank=True,)
    description = models.TextField(default='', blank=True,)

    stock = models.CharField(max_length=100, default='',blank=True,)
    historical_sold = models.CharField(max_length=100, default='',blank=True,)
    liked_count = models.CharField(max_length=100, default='',blank=True,)
    price = models.CharField(max_length=100, default='',blank=True,)
    list_price = models.CharField(max_length=100, default='',blank=True,)
    score = models.CharField(max_length=100, default='',blank=True,)

    def __str__(self):
        return self.name  

class RawProduct(models.Model): 
    url = models.CharField('URL', max_length=512)
    base_encoded_url = models.CharField('Encode URL', max_length=512)
    data = JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

    def extract_data_from_raw(self):  
        info_product = ExtractorService.handle_extract_information_from_json(self.data)
        info_product['base_encoded_url'] = self.base_encoded_url
        if info_product.get('product_code') == 'NONE': return
        
        info_category, created = Category.objects.get_or_create(name=info_product.get('category'))
        if not created: 
            for attr, value in model_to_dict(info_category).items():
                setattr(info_category, attr, value)
            info_category.save()

        info_brand = {
            "name": info_product.get('brand'),
            "category": info_category
        }
        info_brand, created = Brand.objects.get_or_create(**info_brand)
        if not created: 
            for attr, value in model_to_dict(info_brand).items():
                if attr == 'category': setattr(info_brand, attr, info_category)
                else: setattr(info_brand, attr, value)
            info_brand.save()

        product_code = info_product.get('product_code')
        agency = info_product.get('agency') 
        try: 
            info_group_product_db = GroupProduct.objects.get(name__exact=product_code)
            if agency not in info_group_product_db.agencies: info_group_product_db.agencies = info_group_product_db.agencies + [agency]
            info_group_product_db.save()
            info_group_product = info_group_product_db
        except:  
            info_group_product = {
                "name": product_code,
                "category": info_category,
                "agencies": [info_product.get('agency', '')],
                "product_ids": [],
                "quantity": 1
            } 
            print('[CREATE] =>', info_group_product)
            info_group_product, created = GroupProduct.objects.get_or_create(**info_group_product)

        info_product['category'] = info_category
        info_product['brand'] = info_brand
        info_product['group_product'] = info_group_product
        try:
            info_product = Product.objects.get(base_encoded_url=info_product.get('base_encoded_url')) 
            for attr, value in model_to_dict(info_product).items(): 
                if attr == 'category': setattr(info_product, attr, info_category)
                elif attr == 'brand': setattr(info_product, attr, info_brand)
                elif attr == 'group_product': setattr(info_product, attr, info_group_product)
                else: setattr(info_product, attr, value if value else '1')
            info_product.save()
        except:
            info_product, created = Product.objects.get_or_create(**info_product)
            
        product_id = str(info_product.id)
        print('info_group_product', info_group_product.product_ids)
        if product_id not in info_group_product.product_ids: 
            info_group_product.product_ids = info_group_product.product_ids + [product_id]
            info_group_product.quantity = len(info_group_product.product_ids)
            info_group_product.save()

class Scraper(models.Model):
    class ScraperType(models.TextChoices):
        API = 'api', _('API')
        HTML = 'html', _('HTML')

    class SchedulerType(models.TextChoices):
        ONCE = 'once', _('Once')
        HOURLY = 'hourly', _('Hourly')
        DAILY = 'daily', _('Daily')
        # WEEKLY = 'weekly', _('Weekly')
        # MONTHLY = 'month', _('Monthly')
        # YEARLY = 'yearly', _('Yearly')

    class CrawlType(models.TextChoices):
        ALL = 'all', _('All')
        LATEST = 'latest', _('Latest')

    name = models.CharField(max_length=256)
    homepage = models.CharField(max_length=256)
    
    scraper_type = models.CharField(
        max_length=50,
        choices=ScraperType.choices,
        default=ScraperType.API
    )
    crawl_type = models.CharField(
        max_length=50,
        choices=CrawlType.choices,
        default=CrawlType.LATEST
    )
    scheduler_type = models.CharField(
        max_length=50,
        choices=SchedulerType.choices,
        default=SchedulerType.ONCE
    )
    start_time = models.TimeField()
    start_date = models.DateField()
    job_id = models.CharField(max_length=256)
    is_active = models.BooleanField('Active', default=False)
    spiders = models.ManyToManyField(Spider, through='ScraperSpider')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def start_crawling(self): 
        print("[START CRAWLING] =>")
        if self.is_active is False:
            return

        configure_logging()
        crawl_settings = Settings()
        crawl_settings.setmodule('tools.scraper.scraper.settings')
        runner = CrawlerRunner(crawl_settings) 
        for _spider in self.scraperspider_set.all(): 
            runner.crawl(TikiSpider, spider=_spider)

    def update_job(self):
        if self.job_id is not None:
            try:
                scheduler.remove_job(job_id=self.job_id)
            except JobLookupError:
                print("No job")

        job_id = None
        if self.scheduler_type == 'once':
            job_id = scheduler.add_job(
                self.start_crawling,
                trigger='date',
                run_date='{} {}'.format(self.start_date, self.start_time),
            ).id

        if self.scheduler_type == 'hourly':
            job_id = scheduler.add_job(
                self.start_crawling,
                trigger='cron',
                args=[self],
                minute=self.start_time.minute
            ).id

        if self.scheduler_type == 'daily':
            job_id = scheduler.add_job(
                self.start_crawling,
                trigger='cron',
                minute=self.start_time.minute,
                hour=self.start_time.hour
            ).id

        self.job_id = job_id

    def __str__(self):
        return self.name


class ScraperSpider(models.Model):
    scraper = models.ForeignKey(Scraper, on_delete=models.CASCADE)
    spider = models.ForeignKey(Spider, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Parser(models.Model):
    class SelectorType(models.TextChoices):
        XPATH = 'xpath', _('XPATH')
        CSS = 'css', _('CSS')

    name = models.CharField(max_length=256)
    selector_type = models.CharField(
        max_length=50,
        choices=SelectorType.choices,
        default=SelectorType.XPATH
    )
    selector = models.CharField(max_length=256)
    spider = models.ForeignKey(Spider, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Item(models.Model):
    title = models.TextField(null=True)
    content = models.TextField(null=True)
    url = models.TextField()
    author = models.TextField(null=True)
    category = models.TextField(null=True)
    tag = models.TextField(null=True)
    summary = models.TextField(null=True)
    published_at = models.TextField(null=True)
    thumbnail_link = models.TextField(null=True)
    image_link = models.TextField(null=True)
    spider = models.ForeignKey(Spider, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url


class News(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField(null=True)
    url = models.CharField(max_length=256)
    thumbnail_link = models.CharField(max_length=256, null=True)
    image_link = models.CharField(max_length=256, null=True)
    author = models.CharField(max_length=256)
    summary = models.TextField(null=True)
    published_at = models.DateTimeField()
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'News'
 