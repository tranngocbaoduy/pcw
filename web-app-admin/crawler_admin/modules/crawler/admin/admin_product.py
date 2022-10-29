

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin, messages 
from modules.crawler.models.model_product import ( 
    Product,
)

from modules.crawler.filters import ( 
    FilterByCategory,
    FilterByAgency
)

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name", "product_code","agency","price", "updated_at"]
    search_fields = ("name", "agency")
    list_filter = (
        FilterByCategory,
        FilterByAgency,
    )

 