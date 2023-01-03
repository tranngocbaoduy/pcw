import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from modules.crawler.models.utils import id_gen

from tools.scraper.scraper.spiders.html_headless import HtmlHeadless
from tools.scraper.scraper.spiders.html_non_headless import HtmlNonHeadless

class Sitemap(models.Model): 

    class CrawlType(models.TextChoices):
        MPA = "mpa", _("MPA")
        SPA = "spa", _("SPA")

    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
    ) 

    def __str__(self):
        return '#{} - {}'.format(self.id, self.name)

    crawl_type = models.CharField(
        max_length=50, choices=CrawlType.choices, default=CrawlType.MPA
    )

    name = models.CharField(max_length=256) 
    base_url = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PageInfo(models.Model): 

    id = models.CharField(
        primary_key=True, default=id_gen(8), editable=False, unique=True, max_length=12
    ) 

    url = models.CharField(max_length=512)
    title = models.CharField(max_length=512)
    h1 = models.CharField(max_length=512)
    sitemap = models.ForeignKey(Sitemap, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)