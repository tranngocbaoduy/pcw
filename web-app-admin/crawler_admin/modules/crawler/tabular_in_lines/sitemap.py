
from django.contrib import admin, messages
from modules.crawler.models.bot import Scraper, ScraperSitemap
from modules.crawler.models.sitemap import Sitemap, PageInfo
from modules.crawler.forms.sitemap import PageInfoInlineFormSet, SitemapInlineFormSet

class PageInfoTabularInline(admin.TabularInline):
    model = PageInfo
    max_num = 5
    extra = 0
    form = PageInfoInlineFormSet


class ScraperSitemapTabularInline(admin.TabularInline):
    model = ScraperSitemap
    formset = SitemapInlineFormSet