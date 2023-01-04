from import_export.admin import ImportExportModelAdmin
from django.contrib import admin, messages
from modules.crawler.models.parser import Parser, WareParser
from modules.crawler.tabular_in_lines.parser import ParserTabularInline

@admin.register(Parser)
class Parser(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["_id", "name", "selector_type", "selector"]

    def _id(self, obj):
        return '#{}'.format(obj.id)

@admin.register(WareParser)
class WareParser(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["_id", "name"]
    inlines = (ParserTabularInline,)

    def _id(self, obj):
        return '#{}'.format(obj.id)