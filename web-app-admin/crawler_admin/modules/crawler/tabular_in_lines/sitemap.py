
from django.contrib import admin, messages
from modules.crawler.models.sitemap import Sitemap, PageInfo
from modules.crawler.forms.sitemap import PageInfoInlineFormSet

class PageInfoTabularInline(admin.TabularInline):
    model = PageInfo
    formset = PageInfoInlineFormSet
    extra = 0
