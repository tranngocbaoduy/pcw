from import_export.admin import ImportExportModelAdmin
from django.contrib import admin, messages
from modules.crawler.models.product import Category, Product 
from copy import deepcopy

def duplicate(modeladmin, request, queryset):
    for spy in queryset:
        new_obj = deepcopy(spy)
        new_obj.id = None
        new_obj.save() 

duplicate.short_description = "Duplicate"

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["_id", "title", "price", "list_price", "count_update", "updated_at"]
    actions = [duplicate]

    def _id(self, obj):
        return '#{}'.format(obj.id)
    

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["_id", "name", "updated_at"]
    actions = [duplicate]

    def _id(self, obj):
        return '#{}'.format(obj.id)
     