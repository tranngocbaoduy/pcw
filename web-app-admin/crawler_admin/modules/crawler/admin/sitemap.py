from import_export.admin import ImportExportModelAdmin
from django.contrib import admin, messages
from modules.crawler.models.sitemap import Sitemap, PageInfo
from modules.crawler.tabular_in_lines.sitemap import PageInfoTabularInline
from modules.crawler.filters.sitemap import FilterBySitemap

from urllib.parse import urljoin, urlparse
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
class PageInfo(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["_id",  "title", "count_update", "sitemap"]
    list_filter = [FilterBySitemap]
    def _id(self, obj):
        return get_sub_path(obj.url)

    search_fields = ["url"]
     

@admin.register(Sitemap)
class Sitemap(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["_id", "name", "base_url",]
    
    def _id(self, obj):
        return '#{}'.format(obj.id)
        
    inlines = (PageInfoTabularInline,)
    actions = [duplicate]
