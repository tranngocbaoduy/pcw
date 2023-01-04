from gettext import ngettext
from modules.crawler.css_mixin import CSSAdminMixin
# from modules.crawler.apps import scheduler
from mptt.admin import DraggableMPTTAdmin
from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin 

from modules.crawler.models.bot import Scraper
from modules.crawler.tabular_in_lines.sitemap import (
    ScraperSitemapTabularInline,
)


@admin.register(Scraper)
class ScraperAdmin(admin.ModelAdmin, CSSAdminMixin):
    inlines = (ScraperSitemapTabularInline,)
    actions = ["setup_crawler", "stop_crawler"]
    list_display = [
        "_id",
        "name", 
        "scheduler_type",
        "crawl_url",
        "start_time",
        "start_date",
        "is_active", 
    ]
    readonly_fields = ("job_id",)

    def _id(self, obj):
        return '#{}'.format(obj.id)

    def crawl_url(self, obj): 
        return [(spy) for spy in obj.sitemap_cells.all()]

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