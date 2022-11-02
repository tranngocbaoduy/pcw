from django.db.models import JSONField
from modules.crawler.models.utils import id_gen
from django.db import models
from modules.crawler.models.model_category import Category
from django.utils.translation import gettext_lazy as _

from modules.crawler.handlers.extractor import ExtractorService

from scrapy.settings import Settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from tools.scraper.scraper.spiders.api import ApiSpider
from tools.scraper.scraper.spiders.html import HtmlSpider
from tools.scraper.scraper.spiders.html_detail import HtmlSpiderDetail
from tools.scraper.scraper.spiders.html_shopee_detail import HtmlShopeeDetailSpider

from modules.crawler.models.model_spider import Spider
from modules.crawler.models.model_brand import Brand
from modules.crawler.models.model_group_product import GroupProduct
from modules.crawler.models.model_seller import Seller

from django.contrib import  messages

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
    spider = models.ForeignKey(Spider, on_delete=models.CASCADE, blank=True)
    data = JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count_update = models.IntegerField("Count Update", default=1)

    def __str__(self):
        return self.name

    def re_crawl_data(self, request, query):
        print("re_crawl_data")

        configure_logging()
        crawl_settings = Settings()
        crawl_settings.setmodule("tools.scraper.scraper.settings")

        _spider = self.spider
        self.spider.is_running = True
        self.spider.save()
      
        runner = CrawlerRunner(crawl_settings)
            
        # if self.scraper_type == "api":
        #     runner.crawl(ApiSpider, spider=_spider)
        if self.scraper_type == "html":
            runner.crawl(HtmlSpiderDetail, url=self.url, spider=_spider)
        if self.scraper_type == "html_shopee":
            runner.crawl(HtmlShopeeDetailSpider, url=self.url, spider=_spider)

    def extract_data_from_raw(self, request, query):
        print("[REQUEST]=>", self.id)

        from modules.crawler.models.model_product import Product
        info_product = ExtractorService.handle_extract_information_from_json(self.data)
        print("[info_product]=>", info_product)
        info_product["base_encoded_url"] = self.base_encoded_url
        if info_product.get("product_code") == "NONE":
            messages.add_message(
                request,
                messages.WARNING,
                "Get product code {} was failed.".format(self.id),
            )
            return
        
        print('info_category',info_product.get("category"), info_product.get("category_code"))
        if info_product.get("category") or info_product.get("category_code"):
            if info_product.get("category") and type(info_product.get("category")) == dict: 
                print('info_product.get("category")',info_product.get("category"))
                name_category = info_product.get("category").get('name', '')
            if info_product.get("category_code") and type(info_product.get("category_code")) == str: 
                name_category = info_product.get("category_code")
            
            info_category, created = Category.objects.get_or_create(**{'name__exact': name_category })
            
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
            # print("[CREATE] =>", info_group_product)
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

            messages.add_message(
                request,
                messages.SUCCESS,
                "Update {} was success.".format(info_group_product.name),
            )   
        except: 
            try:
                info_product_db, created = Product.objects.get_or_create(**info_product)
                print("CREATE PRODUCT", created)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Create {} was success.".format(info_group_product.name),
                )
            except Exception as err:
                info_product_db = None
                print("CREATE PRODUCT ERR", err)
                messages.add_message(
                    request,
                    messages.WARNING,
                    "Create {} was failed.".format(info_product['name']),
                )
