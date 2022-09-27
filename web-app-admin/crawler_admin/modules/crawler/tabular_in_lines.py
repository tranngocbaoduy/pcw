
from django.contrib import admin, messages
from modules.crawler.models import ScraperSpider, Parser, RawProduct, Product, Brand, Shop, GroupProduct
from modules.crawler.forms import ParserInlineFormSet, ProductInlineFormSet

class ParserTabularInline(admin.TabularInline):
    model = Parser
    formset = ParserInlineFormSet
    extra = 0

class ProductTabularInline(admin.TabularInline):
    model = Product 
    readonly_fields = [f.name for f in model._meta.fields]
    fields = ['clean_name', 'price', 'list_price']
    extra = 0
 
class ScraperSpiderTabularInline(admin.TabularInline):
    model = ScraperSpider
    extra = 0

