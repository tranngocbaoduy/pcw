from import_export.admin import ImportExportModelAdmin
from django.contrib import admin, messages
from modules.crawler.models.sitemap import Sitemap, PageInfo
from modules.crawler.tabular_in_lines.sitemap import PageInfoTabularInline
from modules.crawler.filters.sitemap import FilterBySitemap
from modules.crawler.models.utils import ExtractInfoIphone

from urllib.parse import urljoin, urlparse 
from gettext import ngettext
from copy import deepcopy

def get_sub_path(url):
    o = urlparse(url)
    return o.path

def duplicate(modeladmin, request, queryset):
    for spy in queryset:
        new_obj = deepcopy(spy)
        new_obj.id = None
        new_obj.save() 

duplicate.short_description = "Duplicate"

@admin.register(PageInfo)
class PageInfoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["_id",  "title", "count_update", "sitemap"]
    list_filter = [FilterBySitemap]
    def _id(self, obj):
        return get_sub_path(obj.url)


    search_fields = ["url"]
    actions = [duplicate]

@admin.register(Sitemap)
class SitemapAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["_id", "name", "base_url", "is_crawl_detail_running", "is_sitemap_running", "subscribe"]
    
    def _id(self, obj):
        return '#{}'.format(obj.id)

    def subscribe(self, obj):
        items = PageInfo.objects.filter(sitemap=obj.id)
        total = len(items)
        total_subscribed = len(PageInfo.objects.filter(sitemap=obj.id, is_subscribe=True))
        total_candidates = len([ s for s in items if ExtractInfoIphone.is_candidate_url(s.url, s.title)])
        return '{}/{}/{}'.format(total_subscribed, total_candidates, total)
    
    @admin.action(description="Scan data")
    def scan_data(self, request, queryset):
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
            query.scan_data(request, query)
    
    @admin.action(description="Unsubscribe data")
    def unsubscribe_all(self, request, queryset):
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
            query.unsubscribe_all(request, query)

    inlines = (PageInfoTabularInline,)
    actions = [scan_data, unsubscribe_all, duplicate,]
