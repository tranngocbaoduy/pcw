from import_export.admin import ImportExportModelAdmin
from django.contrib import admin, messages
from modules.crawler.models.sitemap import Sitemap, PageInfo
from modules.crawler.tabular_in_lines.sitemap import PageInfoTabularInline

@admin.register(PageInfo)
class PageInfo(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "url", "title", "h1"]

@admin.register(Sitemap)
class Sitemap(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["_id", "name", "base_url"]

    def _id(self, obj):
        return '#{}'.format(obj.id)
        
    inlines = (PageInfoTabularInline,)
