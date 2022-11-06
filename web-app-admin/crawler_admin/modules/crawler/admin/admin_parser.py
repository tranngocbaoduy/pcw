from import_export.admin import ImportExportModelAdmin
from django.contrib import admin, messages
from modules.crawler.models.model_parser import Parser, ParserWaitUntil


# @admin.register(Parser)
# class Parser(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = ["name", "selector_type", "selector"]

# @admin.register(ParserWaitUntil)
# class ParserWaitUntil(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = ["name", "selector_type", "selector"]
