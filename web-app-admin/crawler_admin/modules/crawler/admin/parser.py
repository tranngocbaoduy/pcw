from import_export.admin import ImportExportModelAdmin
from django.contrib import admin, messages
from modules.crawler.models.parser import Parser, WareParser
from modules.crawler.tabular_in_lines.parser import ParserTabularInline
from copy import deepcopy

def duplicate(modeladmin, request, queryset):
    for spy in queryset:
        new_obj = deepcopy(spy)
        new_obj.id = None
        new_obj.save() 

duplicate.short_description = "Duplicate"

# @admin.register(Parser)
# class ParserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = ["_id", "name", "selector_type", "selector"]
#     actions = [duplicate]

#     def _id(self, obj):
#         return '#{}'.format(obj.id)
    
@admin.register(WareParser)
class WareParserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["_id", "name"]
    inlines = (ParserTabularInline,)
    actions = [duplicate]

    def _id(self, obj):
        return '#{}'.format(obj.id)