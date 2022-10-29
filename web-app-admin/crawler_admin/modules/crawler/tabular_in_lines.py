from django.contrib import admin, messages

from modules.crawler.models.model_parser import Parser
from modules.crawler.models.model_spider import ScraperSpider
from modules.crawler.models.model_raw_product import RawProduct
from modules.crawler.models.model_product import Product
from modules.crawler.models.model_group_product import GroupProduct
 
from modules.crawler.forms import ParserInlineFormSet, ProductInlineFormSet

class ParserTabularInline(admin.TabularInline):
    model = Parser
    formset = ParserInlineFormSet
    extra = 0


class ProductTabularInline(admin.TabularInline):
    model = Product
    readonly_fields = [f.name for f in model._meta.fields]
    fields = ["id", "clean_name", "agency", "price", "list_price"]
    extra = 0


class ScraperSpiderTabularInline(admin.TabularInline):
    model = ScraperSpider
    fields = ["spider", "category"]
    extra = 0
