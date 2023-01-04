from django import forms
from django.apps import apps
from django.forms import BaseInlineFormSet
from modules.crawler.models.sitemap import PageInfo

class PageInfoInlineFormSet(forms.ModelForm):
    class Meta:
        model = PageInfo
        fields = ['url','title', 'meta'] 
        widgets = {
            "url": forms.Textarea(attrs={'rows':3, "cols":42}),
            "title": forms.Textarea(attrs={'rows':3, "cols":42}),
            "meta": forms.Textarea(attrs={'rows': 8}),
        }

class SitemapInlineFormSet(BaseInlineFormSet):
    pass
