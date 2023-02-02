from import_export.admin import ImportExportModelAdmin
from django.contrib import admin, messages
from modules.crawler.models.product import Category, Product, GroupProduct, HistoryPricing
from modules.crawler.tabular_in_lines.product import ProductTabularInline
from modules.crawler.tabular_in_lines.history_pricing import HistoryPricingTabularInline
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
    search_fields = ["id","title"]
    list_display = ["_id", "title", "price", "list_price", "discount_rate", "is_subscribe","count_update", "updated_at"]
    list_filter = [FilterByDomain, FilterByGroup, FilterByCategory]

    inlines = (HistoryPricingTabularInline,)
    
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
   
    @admin.action(description="Update price percentage")
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
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin

admin.site.register(Category, DraggableMPTTAdmin)
# @admin.register(Category, DraggableMPTTAdmin)
# class CategoryAdmin(ImportExportModelAdmin):
#     list_display = ["id", "name", "updated_at"]
#     actions = [duplicate]

#     def _id(self, obj):
#         return '#{}'.format(obj.id)


@admin.register(GroupProduct)
class GroupProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["_id", "name", "category", "updated_at", "subscribers"] 
    list_filter = [FilterByCategory]
    inlines = (ProductTabularInline,)
    def _id(self, obj):
        return '#{}'.format(obj.id)
    
    def subscribers(self, obj):
        return len(Product.objects.filter(group_product=obj.id))     
 
    @admin.action(description="Remove group has 0 subscribers")
    def remove_group_has_0_subscribers(self, request, queryset):
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
            query.remove_group_has_0_subscribers()
    
    @admin.action(description="Update info detail")
    def update_info_detail(self, request, queryset):
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
            query.update_info_detail()

    

    actions = [update_info_detail, remove_group_has_0_subscribers]


# @admin.register(HistoryPricing)
# class HistoryPricingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = ["id","created_at", "price", "list_price", "product"]
    