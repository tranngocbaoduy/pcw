from import_export.admin import ImportExportModelAdmin
from django.contrib import admin, messages
from modules.crawler.models.product import Category, Product, GroupProduct
from modules.crawler.tabular_in_lines.product import ProductTabularInline
from modules.crawler.filters.product import FilterByDomain, FilterByGroup, FilterByCategory
from copy import deepcopy
from gettext import ngettext

def duplicate(modeladmin, request, queryset):
    for spy in queryset:
        new_obj = deepcopy(spy)
        new_obj.id = None
        new_obj.save() 

duplicate.short_description = "Duplicate"

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["_id", "title", "price", "list_price", "discount_rate", "count_update", "updated_at"]
    list_filter = [FilterByDomain, FilterByGroup, FilterByCategory]

    def _id(self, obj):
        return '#{}'.format(obj.id)
    
    @admin.action(description="Categorize")
    def categorize(self, request, queryset):
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
            query.categorize()
   
    @admin.action(description="Update subscription")
    def check_subscribe(self, request, queryset):
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
            query.check_subscribe()
    
    
    actions = [categorize, check_subscribe]
    

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["_id", "name", "updated_at"]
    actions = [duplicate]

    def _id(self, obj):
        return '#{}'.format(obj.id)


@admin.register(GroupProduct)
class GroupProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["_id", "name", "category", "updated_at", "subscribers"] 
    list_filter = [FilterByCategory]
    inlines = (ProductTabularInline,)
    def _id(self, obj):
        return '#{}'.format(obj.id)
    
    def subscribers(self, obj):
        return len(Product.objects.filter(group_product=obj.id))     