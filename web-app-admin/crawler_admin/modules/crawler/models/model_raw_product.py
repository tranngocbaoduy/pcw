from django.db.models import JSONField
from modules.crawler.models.utils import id_generator
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

from django.contrib import messages


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
        primary_key=True, default=id_generator, editable=False, unique=True, max_length=12
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

        try:
            info_product = ExtractorService.handle_extract_information_from_json(self.data)
            info_product["base_encoded_url"] = self.base_encoded_url

            info_category = create_or_update(Category, "name", info_product['category_code'], {
                "name": info_product['category_code']
            })
            info_product['category'] = info_category
            del info_product['category_code'] 
            

            print("[info_product]=>", info_product) 
            create_or_update(Product, "base_encoded_url", info_product['base_encoded_url'], info_product)
        

            # Category information by product code

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

            info_product["group_product"] = info_group_product
            create_or_update(Product, "group_product", info_product["group_product"], info_product)
        except Exception as e:
            print(e)
            messages.add_message(
                request,
                messages.WARNING,
                "Transfer product failed #{}.".format(self.id),
            )

    