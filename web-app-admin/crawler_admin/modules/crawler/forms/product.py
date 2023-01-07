from django import forms
from django.apps import apps
from django.forms import BaseInlineFormSet
from modules.crawler.models.product import Product

class ProductInlineFormSet(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['base_url','title', 'price', 'list_price'] 
        widgets = {
            "base_url": forms.Textarea(attrs={'rows':2, "cols":42}),
            "title": forms.Textarea(attrs={'rows':2, "cols":42}),
            "price": forms.Textarea(attrs={'rows': 2, "cols":15}),
            "list_price": forms.Textarea(attrs={'rows': 2, "cols":15}),
        }
 