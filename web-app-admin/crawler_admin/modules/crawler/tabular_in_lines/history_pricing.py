
from django.contrib import admin, messages 
from modules.crawler.models.product import HistoryPricing
from modules.crawler.forms.history_pricing import HistoryPricingInlineFormSet

class HistoryPricingTabularInline(admin.TabularInline):
    model = HistoryPricing
    form = HistoryPricingInlineFormSet
    extra = 0
 