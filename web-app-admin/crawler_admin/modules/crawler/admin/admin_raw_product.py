from gettext import ngettext
from import_export.admin import ImportExportModelAdmin
from modules.crawler.format.json_admin import JsonAdmin
from django.contrib import admin, messages

from modules.crawler.filters import (
    FilterByAgency,
)
from modules.crawler.models.model_brand import Brand
from modules.crawler.models.model_category import Category
from modules.crawler.models.model_raw_product import RawProduct
from django.utils.html import mark_safe
from price_parser import Price
from decimal import Decimal

@admin.register(RawProduct)
class RawProductAdmin(ImportExportModelAdmin, JsonAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "agency",
        "price", 
        "count_update", 
        "updated_at",
    ]
    search_fields = ("name", "agency")
    list_filter = (FilterByAgency,)

    def price(self, obj):
        money = obj.data.get("price")
        if money:  
            return '{:20,.0f}'.format(money)+ " vnđ"
        return ''

    actions = ["extract_info", "re_crawl"]
    

    class Media:
        css = {"all": ("css/fancy.css",)}

    @admin.action(description="Extract Infomation")
    def extract_info(self, request, queryset):
        self.message_user(
            request,
            ngettext(
                "%d was successfully running.",
                "%d were successfully running.",
                len(queryset),
            )
            % len(queryset),
            messages.SUCCESS,
        )
        for query in queryset:
            query.extract_data_from_raw(request, query)

    @admin.action(description="Re-crawl data")
    def re_crawl(self, request, queryset):
        self.message_user(
            request,
            ngettext(
                "%d was successfully running.",
                "%d were successfully running.",
                len(queryset),
            )
            % len(queryset),
            messages.SUCCESS,
        )
        for query in queryset:
            query.re_crawl_data(request, query)
