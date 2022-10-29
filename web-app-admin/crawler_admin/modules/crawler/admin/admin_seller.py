

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin, messages 
from modules.crawler.models.model_seller import ( 
    Seller,
)

from modules.crawler.filters import ( 
    FilterByAgency
)

@admin.register(Seller)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["name", "address", "url", "agency", "created_at"] 
    list_filter = ( 
        FilterByAgency,
    )
