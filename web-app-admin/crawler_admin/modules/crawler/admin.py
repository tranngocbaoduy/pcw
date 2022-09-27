from gettext import ngettext
from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin

from modules.crawler.apps import scheduler
from modules.crawler.models import Spider, Scraper, ScraperSpider, Category, Parser, Item, News, RawProduct, Product, Brand, Shop, GroupProduct
from import_export import resources


from modules.crawler.filters import FilterByCategory, FilterByDomain, FilterByAgency
from modules.crawler.tabular_in_lines import ParserTabularInline, ProductTabularInline, ScraperSpiderTabularInline

# Register your models here. 

@admin.register(Spider)
class SpiderAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain', 'url', 'total_items']
    inlines = (
        ParserTabularInline,
    )

    def total_items(self, obj):
        return obj.item_set.count()

    total_items.short_description = 'Total Items'

@admin.register(Scraper)
class ScraperAdmin(admin.ModelAdmin):
    inlines = (
        ScraperSpiderTabularInline,
    )

    actions = ['setup_crawler', 'stop_crawler']
    list_display = ['name', 'scraper_type', 'scheduler_type', 'start_time', 'start_date', 'is_active']
    readonly_fields = ('job_id',)

    @admin.action(description='Start crawling now')
    def setup_crawler(self, request, queryset):
        for query in queryset:
            query.start_crawling()

        self.message_user(request, ngettext(
            '%d scraper was successfully running.',
            '%d scrapers were successfully running.',
            len(queryset),
        ) % len(queryset), messages.SUCCESS)

    @admin.action(description='Disable crawler')
    def disable_crawler(self, request, queryset):
        for query in queryset:
            scheduler.remove_job(query.job_id)
        self.message_user(request, ngettext(
            '%d scraper was successfully disabled.',
            '%d scrapers were successfully disbled.',
            len(queryset),
        ) % len(queryset), messages.SUCCESS)

    @admin.action(description='Enable crawler')
    def enable_crawler(self, request, queryset):
        for query in queryset:
            query.create_job()
        self.message_user(request, ngettext(
            '%d scraper was successfully disabled.',
            '%d scrapers were successfully disbled.',
            len(queryset),
        ) % len(queryset), messages.SUCCESS)

@admin.register(RawProduct)
class RawProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['url', 'created_at', 'updated_at']  

    actions = ['extract_info']
    @admin.action(description='Extract Infomation')
    def extract_info(self, request, queryset):
        for query in queryset:
            query.extract_data_from_raw()

        self.message_user(request, ngettext(
            '%d was successfully running.',
            '%d were successfully running.',
            len(queryset),
        ) % len(queryset), messages.SUCCESS)
    
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'domain', 'category', 'price','created_at'] 
    list_filter = (FilterByCategory, FilterByAgency, )
     
admin.site.register(Brand)
admin.site.register(Shop) 

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']

    actions = ['group_product_by_code']
    @admin.action(description='Group Product By Code')
    def group_product_by_code(self, request, queryset):
        for query in queryset:
            query.group_product_by_code()

        self.message_user(request, ngettext(
            '%d was successfully running.',
            '%d were successfully running.',
            len(queryset),
        ) % len(queryset), messages.SUCCESS)

@admin.register(GroupProduct)
class GroupProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'quantity', 'category', 'agencies']
    list_filter = (FilterByCategory, FilterByAgency)
    inlines = (
        ProductTabularInline,
    )
    
    
