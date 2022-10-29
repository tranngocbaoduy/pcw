

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin, messages 
from modules.crawler.models.model_product import Product
from modules.crawler.models.model_group_product import GroupProduct

from modules.crawler.tabular_in_lines import (
    ProductTabularInline, 
)

from modules.crawler.filters import ( 
    FilterByCategory,
    FilterByAgency
)

@admin.register(GroupProduct)
class GroupProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name", "category", "agencies", "total_items"]
    search_fields = ("name", "category", "agencies")
    list_filter = (FilterByCategory, FilterByAgency)
    inlines = (ProductTabularInline,)

    def total_items(self, obj):
        products = Product.objects.filter(group_product=obj)
        return len(products)

    total_items.short_description = "Total Items"
