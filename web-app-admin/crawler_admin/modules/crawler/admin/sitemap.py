from import_export.admin import ImportExportModelAdmin
from django.contrib import admin, messages
from modules.crawler.models.sitemap import Sitemap, PageInfo
from modules.crawler.tabular_in_lines.sitemap import PageInfoTabularInline
from modules.crawler.filters.sitemap import FilterBySitemap
from modules.crawler.models.utils import ExtractInfoIphone, ExtractInfoMacbook, ExtractInfoAppleWatch
from modules.crawler.filters.sitemap import FilterByCategory
from modules.crawler.admin.parser import WareParserResource

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


from import_export import resources, widgets, fields

class SitemapResource(resources.ModelResource):
    sitemap = fields.Field(
        column_name='sitemap_id',
        attribute='sitemap',
        widget=widgets.ForeignKeyWidget(Sitemap, 'id'))
     
    class Meta:
        model = Sitemap  

@admin.register(PageInfo)
class PageInfoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["id",  "sub_url", "title", "count_update", "sitemap"]
    list_filter = [FilterBySitemap]
    resources_class = SitemapResource
    def sub_url(self, obj):
        return get_sub_path(obj.url)


    search_fields = ["url"]
    actions = [duplicate]

@admin.register(Sitemap)
class SitemapAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["_id", "name", "category_name", "base_url", "is_crawl_detail_running", "is_sitemap_running", "subscribe"]
    list_filter = [FilterByCategory]
    resources_class = WareParserResource
    
    def _id(self, obj):
        return '#{}'.format(obj.id)

    def subscribe(self, obj):
        items = PageInfo.objects.filter(sitemap=obj.id)
        total = len(items)
        total_subscribed = len(PageInfo.objects.filter(sitemap=obj.id, is_subscribe=True))
        total_candidates = 0
        if obj.category_name == 'iPhone':
            total_candidates = len(list(filter(lambda x: ExtractInfoIphone.is_candidate_url(x.url, x.title), items)))
        elif obj.category_name == 'Macbook':
            total_candidates = len(list(filter(lambda x: ExtractInfoMacbook.is_candidate_url(x.url, x.title), items)))
        elif obj.category_name == 'Apple Watch':
            total_candidates = len(list(filter(lambda x: ExtractInfoAppleWatch.is_candidate_url(x.url, x.title), items)))
        
        return '{}/{}/{}'.format(total_subscribed, total_candidates, total)
    
    @admin.action(description="Scan sub page data")
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

    # inlines = (PageInfoTabularInline,)
    actions = [scan_data, unsubscribe_all, duplicate,]
