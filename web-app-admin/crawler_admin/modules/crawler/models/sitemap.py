import uuid
from django.db.models import JSONField
from django.db import models
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from modules.crawler.models.utils import id_generator, id_gen, ExtractInfoIphone, ExtractInfoMacbook
from modules.crawler.models.parser import WareParser

from tools.scraper.scraper.spiders.html_headless import HtmlHeadless
from tools.scraper.scraper.spiders.html_headless_detail import HtmlHeadlessDetail
from tools.scraper.scraper.spiders.html_non_headless import HtmlNonHeadless

from scrapy.settings import Settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
 
class Sitemap(models.Model): 

    class CrawlType(models.TextChoices):
        MPA = "mpa", _("MPA")
        SPA = "spa", _("SPA")

    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
    ) 

    def __str__(self):
        return '#SI{} - {}'.format(self.id, self.name)

    crawl_type = models.CharField(
        max_length=50, choices=CrawlType.choices, default=CrawlType.MPA
    )

    name = models.CharField(max_length=256) 
    base_url = models.CharField(max_length=256)
    target_search_terms = models.CharField(max_length=512, default="apple-iphone-,iphone-14,iphone-13,iphone-12,iphone-11,iphone-se", blank=True)
    exclude_search_terms = models.CharField(max_length=512, default="dat-truoc,su-kien,event,quay-,tai-nghe,&,filter,loc,so-sanh,san-pham-moi,cong-nghe,nguoi-,khuyen-mai,phu-kien,combo,tag,dchannel,tragop,zalo,tra-gop,news,tekzone,the-,hub-,cap-,cuong-luc,bao-,mieng-,sac-,op-,mua-", blank=True)
    ware_parser = models.ForeignKey(WareParser, on_delete=models.CASCADE, null=True)
    is_sitemap_running = models.BooleanField(default=False, editable=False)
    is_crawl_detail_running = models.BooleanField(default=False, editable=False)
    category_name = models.CharField(max_length=256, default="")
    limit_page = models.CharField(max_length=256, default="500")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def scan_data(self, request, query):
        if self.is_crawl_detail_running: 
            self.save()
            messages.add_message(
                request,
                messages.WARNING,
                "Scan data #{} is running.".format(self.id),
            )
        else: 
            configure_logging()
            crawl_settings = Settings()
            crawl_settings.setmodule("tools.scraper.scraper.settings")

            if self.category_name == 'Điện thoại':
                page_info_items = PageInfo.objects.filter(sitemap=self.id)#is_subscribe=True
                page_info_items = list(filter(lambda x: ExtractInfoIphone.is_candidate_url(x.url, x.title), page_info_items))
            elif self.category_name == 'Macbook':
                page_info_items = PageInfo.objects.filter(sitemap=self.id)#is_subscribe=True
                page_info_items = list(filter(lambda x: ExtractInfoMacbook.is_candidate_url(x.url, x.title), page_info_items))
            else:
                page_info_items = []

            if page_info_items and len(page_info_items) != 0:
                self.is_crawl_detail_running = True
                self.save()
                
                runner = CrawlerRunner(crawl_settings)
                runner.crawl(HtmlHeadlessDetail, sitemap=self, page_info_items=page_info_items)
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "No data to scan",
                ) 

    def unsubscribe_all(self, request, query):
        page_info_items = PageInfo.objects.filter(sitemap=self.id)#is_subscribe=True
        for page_info in page_info_items:
            page_info.is_subscribe = False
            page_info.save()

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
    is_subscribe = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '#PA{} - {}'.format(self.id, self.title)

    class Meta:
        ordering = ['title']