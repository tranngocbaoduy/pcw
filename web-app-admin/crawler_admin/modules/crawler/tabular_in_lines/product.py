
from django.contrib import admin, messages 
from modules.crawler.models.product import Product
from modules.crawler.forms.product import ProductInlineFormSet

class ProductTabularInline(admin.TabularInline):
    model = Product
    form = ProductInlineFormSet
    extra = 0
 