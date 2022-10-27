import json
import logging
import uuid
from apscheduler.jobstores.base import JobLookupError
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.contrib import messages

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from scrapy.settings import Settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from modules.crawler.apps import scheduler
from tools.scraper.scraper.spiders.api import ApiSpider
from tools.scraper.scraper.spiders.html import HtmlSpider
from tools.scraper.scraper.spiders.html_shopee import HtmlShopeeSpider
from modules.crawler.handlers.extractor import ExtractorService

def id_gen(ID_LENGTH=6) -> str: 
    """Generates random string whose length is `ID_LENGTH`"""
    return str(uuid.uuid4().int)[:ID_LENGTH]

class ParserWaitUntil(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    class SelectorType(models.TextChoices):
        XPATH = "xpath", _("XPATH")
        CSS = "css", _("CSS")

    name = models.CharField(max_length=256)
    selector_type = models.CharField(
        max_length=50, choices=SelectorType.choices, default=SelectorType.XPATH
    )
    selector = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Spider(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=256)
    url = models.CharField("URL", max_length=512)
    is_using_proxy = models.BooleanField("Using Proxy", default=False)
    class_parent = models.CharField("Class Parent", max_length=256, blank=True)
    class_child = models.CharField("Class Child", max_length=256, blank=True)
    limit_per_request = models.IntegerField("Limit per page", default=30)
    start_page = models.IntegerField("Start page", default=0)
    end_page = models.IntegerField("End page", default=100)
    base_url_item = models.CharField(
        "Base url item", default="", max_length=256, blank=True
    ) 
    is_headless = models.BooleanField("Not using browser", default=True, editable=True)
    domain = models.CharField("Domain", default="", max_length=256)
    agency = models.CharField("Agency", default="", max_length=256)
    parser_wait_until_parent = models.ForeignKey(ParserWaitUntil, on_delete=models.CASCADE, editable=True, null=True, blank=True, related_name='spirder_parser_parent')
    parser_wait_until_child = models.ForeignKey(ParserWaitUntil, on_delete=models.CASCADE, editable=True, null=True, blank=True, related_name='spirder_parser_child')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_running = models.BooleanField("Is running", default=False, editable=False)

    def __str__(self):
        return self.name


class Category(MPTTModel):
    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
    )
    name = models.CharField(max_length=250)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    vi_name = models.CharField(max_length=250, default='', blank=True, null=True)
    en_name = models.CharField(max_length=250, default='', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def group_product_by_code(self):
        list_product = Product.objects.filter(category=self.id)
        list_product_code = [product.product_code for product in list_product]
        stat = self.handle_stat_group(list_product_code)
        for name, quantity in stat.items():
            info_group_product = {
                "category": self,
                "name": name,
            }
            info_group_product, created = GroupProduct.objects.get_or_create(
                **info_group_product
            )
            if not created:
                # print({"message":'[UPDATE BRAND]', "info_brand": model_to_dict(info_brand)})
                for attr, value in model_to_dict(info_brand).items():
                    if attr == "category":
                        setattr(info_brand, attr, self)
                    else:
                        setattr(info_brand, attr, value)
                info_brand.save()
        print("[GROUP {} PRODUCT ITEMS]".format(len(list_product)), stat)

    def handle_stat_group(self, texts):
        stat_group = {}
        for i in texts:
            if i not in stat_group:
                stat_group[i] = 1
            else:
                stat_group[i] += 1
        return stat_group


class Brand(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.category.name, self.name)


class Seller(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=256, blank=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    review =  models.IntegerField(default=0, null=True)
    star = models.FloatField(default=0, blank=True, null=True)
    image =  models.CharField(max_length=256, blank=True, null=True)
    agency = models.CharField(max_length=256, blank=True)
    url = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.agency)


class GroupProduct(models.Model):
    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
    )
    name = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    agencies = ArrayField(
        ArrayField(
            models.CharField(max_length=10, blank=True),
            size=10,
            blank=True,
        ),
        size=100,
        default=list,
    ) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)

def create_or_update(model, query, query_data, data):
    params = {}
    params[query] = query_data
    result = model.objects.filter(**params).first()
    if result:
        print("Update ...")
        for k, v in data.items():
            foreign_model = model._meta.get_field(k).related_model
            if foreign_model:
                continue
            else:
                setattr(result, k, v)
        result.save()
    else:
        print("Create new ...") 
        result = model.objects.create(**data)
    return result

class RawProduct(models.Model):
    class ScraperType(models.TextChoices):
        API = "api", _("API")
        HTML = "html", _("HTML")
        HTML_SHOPEE = "html_shopee", _("HTML_SHOPEE")
 
    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
    )
    url = models.CharField("URL", max_length=512)
    name = models.CharField("Name", max_length=512, blank=True)
    agency = models.CharField("Agency", max_length=512, blank=True)
    base_encoded_url = models.CharField("Encode URL", max_length=512)
    scraper_type = models.CharField(
        max_length=50, choices=ScraperType.choices, default=ScraperType.API
    )
    data = JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count_update = models.IntegerField("Count Update", default=1)

    def __str__(self):
        return self.name

    def extract_data_from_raw(self, request, query):
        print("[REQUEST]=>", id_gen())
        info_product = ExtractorService.handle_extract_information_from_json(self.data)
        print("info_product", info_product)
        info_product["base_encoded_url"] = self.base_encoded_url
        if info_product.get("product_code") == "NONE":
            return
        
        if info_product.get("category"):
            if info_product.get("category") and type(info_product.get("category")) == dict: 
                name_category = info_product.get("category").name
            if info_product.get("category") and type(info_product.get("category")) == str: 
                name_category = info_product.get("category")
            
            info_category, created = Category.objects.get_or_create(**{'name__exact': name_category })
            print('info_category',info_category)
            info_product["category"] = info_category

        # print(3)
        if info_product.get("tree_category"):
            tree_category = info_product.get("tree_category", [])
            for category in tree_category: 
                name_category_parent = category.get('parent', '')
                name_category_current = category.get('name') 
                name_category_child = category.get('child')
                if name_category_child:
                    if name_category_current and name_category_parent == '':
                        Category.objects.get_or_create(**{"name": name_category_current})
                    elif name_category_current and name_category_parent:
                        info_child = Category.objects.filter(**{"name": name_category_current}).first()
                        if info_child == None:
                            info_child = Category.objects.create(**{"name": name_category_current})

                        info_parent = Category.objects.filter(**{"name": name_category_parent}).first()
                        if info_parent:
                            info_child.parent = info_parent
                            info_child.save()
                        else:
                            info_parent = Category.objects.create(**{"name": name_category_parent})
                            info_child.parent = info_parent
                            info_child.save() 
                print("==\n")
            del info_product['tree_category']
             
        if info_product.get("brand"):
            name_brand = info_product.get("brand")
            info_brand = {"name": name_brand, "category": info_category}
            info_brand = create_or_update(Brand, 'name', name_brand, info_brand)
            info_product["brand"] = info_brand

        product_code = info_product.get("product_code")
        agency = info_product.get("agency")
       
        try:
            info_group_product_db = GroupProduct.objects.get(name__exact=product_code)
            if agency not in info_group_product_db.agencies:
                info_group_product_db.agencies = info_group_product_db.agencies + [
                    agency
                ]
            info_group_product_db.save()
            info_group_product = info_group_product_db
        except:
            info_group_product = {
                "name": product_code,
                "category": info_category,
                "agencies": [info_product.get("agency", "")], 
            }
            print("[CREATE] =>", info_group_product)
            info_group_product, created = GroupProduct.objects.get_or_create(
                **info_group_product
            )
        
        if info_product.get("seller"):
            info_seller = info_product.get('seller')  
            info_seller['agency'] = info_product.get('domain', '') 
            info_seller = create_or_update(Seller, 'name', info_seller['name'], info_seller)            
            info_product["seller"] = info_seller


        info_product["group_product"] = info_group_product
        info_product["id_raw_product"] = query
        try:
            info_product_db = Product.objects.get(
                base_encoded_url=info_product.get("base_encoded_url")
            )
            print("UPDATE PRODUCT", info_product)

            for attr, value in info_product.items():
                if attr == "id": continue
                elif attr == "category":
                    setattr(info_product_db, attr, info_category)
                elif attr == "brand":
                    setattr(info_product_db, attr, info_brand)
                elif attr == "group_product":
                    setattr(info_product_db, attr, info_group_product)
                elif attr == "id_raw_product":
                    print("query", query)
                    setattr(info_product_db, attr, query)
                else:
                    print('a', attr, value)
                    setattr(info_product_db, attr, value if value else "1")
            info_product_db.save()
        except: 
            try:
                info_product_db, created = Product.objects.get_or_create(**info_product)
                print("CREATE PRODUCT", created)
            except Exception as err:
                info_product_db = None
                print("CREATE PRODUCT ERR", err)
 


class Product(models.Model):
    class ScraperType(models.TextChoices):
        API = "api", _("API")
        HTML = "html", _("HTML")
        HTML_SHOPEE = "html_shopee", _("HTML_SHOPEE")
    
    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
    ) 
    name = models.CharField("Name", max_length=256)
    clean_name = models.CharField("Clean Name", max_length=256)
    url = models.CharField("URL", max_length=512)
    base_encoded_url = models.CharField("Encode URL", max_length=512)
    domain = models.CharField("Domain", max_length=256)
    agency = models.CharField("Agency", max_length=256)
    product_code = models.CharField("Code", max_length=256)
    scraper_type = models.CharField(
        max_length=50, choices=ScraperType.choices, default=ScraperType.API
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    id_raw_product = models.ForeignKey(
        RawProduct, blank=True, null=True, on_delete=models.CASCADE
    )
    group_product = models.ForeignKey(
        GroupProduct, blank=True, null=True, on_delete=models.CASCADE
    ) 
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    count_update = models.IntegerField("Count Update", default=0)

    slug_id = models.CharField("Slug Id", max_length=1024, blank=True)
    image = models.TextField(
        default="",
        blank=True,
    ) 
    item_rating = models.TextField(
        default="",
        blank=True,
    )
    description = models.TextField(
        default="",
        blank=True,
    )

    stock = models.CharField(
        max_length=100,
        default="",
        blank=True,
    )
    historical_sold = models.CharField(
        max_length=100,
        default="",
        blank=True,
    )
    liked_count = models.CharField(
        max_length=100,
        default="",
        blank=True,
    )
    price = models.CharField(
        max_length=100,
        default="",
        blank=True,
    )
    list_price = models.CharField(
        max_length=100,
        default="",
        blank=True,
    )
    score = models.CharField(
        max_length=100,
        default="",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Scraper(models.Model):
    class ScraperType(models.TextChoices):
        API = "api", _("API")
        HTML = "html", _("HTML")
        HTML_SHOPEE = "html_shopee", _("HTML_SHOPEE")

    class SchedulerType(models.TextChoices):
        ONCE = "once", _("Once")
        HOURLY = "hourly", _("Hourly")
        DAILY = "daily", _("Daily")
        # WEEKLY = 'weekly', _('Weekly')
        # MONTHLY = 'month', _('Monthly')
        # YEARLY = 'yearly', _('Yearly')

    class CrawlType(models.TextChoices):
        ALL = "all", _("All")
        LATEST = "latest", _("Latest")

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=256)
    homepage = models.CharField(max_length=256)

    scraper_type = models.CharField(
        max_length=50, choices=ScraperType.choices, default=ScraperType.API
    )
    crawl_type = models.CharField(
        max_length=50, choices=CrawlType.choices, default=CrawlType.LATEST
    )
    scheduler_type = models.CharField(
        max_length=50, choices=SchedulerType.choices, default=SchedulerType.ONCE
    )
    start_time = models.TimeField()
    start_date = models.DateField()
    job_id = models.CharField(max_length=256)
    is_active = models.BooleanField("Active", default=False)
    spiders = models.ManyToManyField(Spider, through="ScraperSpider")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def start_crawling(self):
        if self.is_active is False:
            return

        configure_logging()
        crawl_settings = Settings()
        crawl_settings.setmodule("tools.scraper.scraper.settings")

        for _spider in self.scraperspider_set.all():
            spider_db = _spider.spider
            params = {}
            if spider_db.is_headless:
                params["SELENIUM_DRIVER_ARGUMENTS"] = ['--headless']
            else: params["SELENIUM_DRIVER_ARGUMENTS"] = []
            crawl_settings.update(params)
            runner = CrawlerRunner(crawl_settings)
            
            spider_db.is_running = True
            spider_db.save()
            if self.scraper_type == "api":
                runner.crawl(ApiSpider, spider=_spider)
            if self.scraper_type == "html":
                runner.crawl(HtmlSpider, spider=_spider)
            if self.scraper_type == "html_shopee":
                runner.crawl(HtmlShopeeSpider, spider=_spider)

    def update_job(self):
        if self.job_id is not None:
            try:
                scheduler.remove_job(job_id=self.job_id)
            except JobLookupError:
                print("No job")

        job_id = None
        if self.scheduler_type == "once":
            job_id = scheduler.add_job(
                self.start_crawling,
                trigger="date",
                run_date="{} {}".format(self.start_date, self.start_time),
            ).id

        if self.scheduler_type == "hourly":
            job_id = scheduler.add_job(
                self.start_crawling,
                trigger="cron",
                args=[self],
                minute=self.start_time.minute,
            ).id

        if self.scheduler_type == "daily":
            job_id = scheduler.add_job(
                self.start_crawling,
                trigger="cron",
                minute=self.start_time.minute,
                hour=self.start_time.hour,
            ).id

        self.job_id = job_id

    def __str__(self):
        return self.name


class ScraperSpider(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    scraper = models.ForeignKey(Scraper, on_delete=models.CASCADE)
    spider = models.ForeignKey(Spider, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.spider.name, self.spider.is_running)

class Parser(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    class SelectorType(models.TextChoices):
        XPATH = "xpath", _("XPATH")
        CSS = "css", _("CSS")

    name = models.CharField(max_length=256)
    selector_type = models.CharField(
        max_length=50, choices=SelectorType.choices, default=SelectorType.XPATH
    )
    selector = models.CharField(max_length=256)
    spider = models.ForeignKey(Spider, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
