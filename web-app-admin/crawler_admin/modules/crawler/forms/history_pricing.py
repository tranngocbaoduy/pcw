from django import forms
from django.apps import apps
from django.forms import BaseInlineFormSet
from modules.crawler.models.product import HistoryPricing

class HistoryPricingInlineFormSet(forms.ModelForm):
    class Meta:
        model = HistoryPricing
        fields = ['created_at','price', 'list_price'] 
        widgets = {
            "created_at": forms.Textarea(attrs={'rows':2, "cols":42}), 
            "price": forms.Textarea(attrs={'rows': 2, "cols":15}),
            "list_price": forms.Textarea(attrs={'rows': 2, "cols":15}),
        }
 