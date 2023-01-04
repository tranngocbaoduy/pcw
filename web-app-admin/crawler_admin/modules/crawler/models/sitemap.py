import uuid
from django.db.models import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _
from modules.crawler.models.utils import id_generator, id_gen

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
    target_search_terms = models.CharField(max_length=512, default="apple-iphone-,iphone-14,iphone-13,iphone-12,iphone-11,iphone-se", blank=True)
    exclude_search_terms = models.CharField(max_length=512, default="dat-truoc,su-kien,event,quay-,tai-nghe,&,filter,loc,so-sanh,san-pham-moi,cong-nghe,nguoi-,khuyen-mai,phu-kien,combo,tag,dchannel,tragop,zalo,tra-gop,news,tekzone,the-,hub-,cap-,cuong-luc,bao-,mieng-,sac-,op-,mua-", blank=True)
    limit_page = models.CharField(max_length=256, default="500")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

class PageInfo(models.Model): 

    id = models.CharField(
        primary_key=True, default=id_generator, editable=False, unique=True, max_length=12
    ) 

    url = models.CharField(max_length=512)
    title = models.CharField(max_length=512)
    encoded_base_url = models.CharField(max_length=512)
    meta = JSONField(default=dict)
    sitemap = models.ForeignKey(Sitemap, on_delete=models.CASCADE)
    count_update = models.IntegerField(default=1, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '#{} - {}'.format(self.id, self.title)

    class Meta:
        ordering = ['title']