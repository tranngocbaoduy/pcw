from gettext import ngettext
from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin

from modules.crawler.apps import scheduler
from modules.crawler.format.json_admin import JsonAdmin
from modules.crawler.models import (
    Spider,
    Scraper,
    ScraperSpider,
    Category,
    Parser,
    RawProduct,
    Product,
    Brand,
    Shop,
    GroupProduct,
)
from import_export import resources


from modules.crawler.filters import (
    FilterByCategory,
    FilterByDomain,
    FilterByAgency,
    FilterByAgencyUrl,
)
from modules.crawler.tabular_in_lines import (
    ParserTabularInline,
    ProductTabularInline,
    ScraperSpiderTabularInline,
)

# Register your models here.
@admin.register(Spider)
class SpiderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name", "domain", "url", "base_url_item", "updated_at"]
    search_fields = ("name", "domain")
    inlines = (ParserTabularInline,)


@admin.register(Scraper)
class ScraperAdmin(admin.ModelAdmin):
    inlines = (ScraperSpiderTabularInline,)

    actions = ["setup_crawler", "stop_crawler"]
    list_display = [
        "id",
        "name",
        "scraper_type",
        "scheduler_type",
        "crawl_url",
        "start_time",
        "start_date",
        "is_active",
    ]
    readonly_fields = ("job_id",)

    def crawl_url(self, obj):
        return [ spy.url for spy in obj.spiders.all()]

    @admin.action(description="Start crawling now")
    def setup_crawler(self, request, queryset):
        for query in queryset:
            query.start_crawling()

        self.message_user(
            request,
            ngettext(
                "%d scraper was successfully running.",
                "%d scrapers were successfully running.",
                len(queryset),
            )
            % len(queryset),
            messages.SUCCESS,
        )

    @admin.action(description="Disable crawler")
    def disable_crawler(self, request, queryset):
        for query in queryset:
            scheduler.remove_job(query.job_id)
        self.message_user(
            request,
            ngettext(
                "%d scraper was successfully disabled.",
                "%d scrapers were successfully disbled.",
                len(queryset),
            )
            % len(queryset),
            messages.SUCCESS,
        )

    @admin.action(description="Enable crawler")
    def enable_crawler(self, request, queryset):
        for query in queryset:
            query.create_job()
        self.message_user(
            request,
            ngettext(
                "%d scraper was successfully disabled.",
                "%d scrapers were successfully disbled.",
                len(queryset),
            )
            % len(queryset),
            messages.SUCCESS,
        )


@admin.register(RawProduct)
class RawProductAdmin(ImportExportModelAdmin, JsonAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "agency",
        "scraper_type",
        "count_update",
        "updated_at",
    ]
    search_fields = ("name", "agency")
    list_filter = (FilterByAgency,)

    actions = ["extract_info"]

    class Media:
        css = {"all": ("css/fancy.css",)}

    @admin.action(description="Extract Infomation")
    def extract_info(self, request, queryset):
        for query in queryset:
            query.extract_data_from_raw(request)

        # self.message_user(
        #     request,
        #     ngettext(
        #         "%d was successfully running.",
        #         "%d were successfully running.",
        #         len(queryset),
        #     )
        #     % len(queryset),
        #     messages.SUCCESS,
        # )


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name", "agency", "category", "price", "updated_at"]
    search_fields = ("name", "agency", "category")
    list_filter = (
        FilterByCategory,
        FilterByAgency,
    )


admin.site.register(Brand)
admin.site.register(Shop)
admin.site.site_header = "Meteor System"
admin.site.site_title = "Meteor System"


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name", "updated_at"]
    search_fields = ("name", "id")
    actions = ["group_product_by_code"]

    @admin.action(description="Group Product By Code")
    def group_product_by_code(self, request, queryset):
        for query in queryset:
            query.group_product_by_code()

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


@admin.register(GroupProduct)
class GroupProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name", "category", "agencies", "total_items"]
    search_fields = ("name", "category", "agencies")
    list_filter = (FilterByCategory, FilterByAgency)
    inlines = (ProductTabularInline,)

    def total_items(self, obj):
        return len(obj.product_ids)

    total_items.short_description = "Total Items"
