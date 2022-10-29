
import uuid
from django.db import models

from apscheduler.jobstores.base import JobLookupError
from modules.crawler.apps import scheduler

from scrapy.settings import Settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from tools.scraper.scraper.spiders.api import ApiSpider
from tools.scraper.scraper.spiders.html import HtmlSpider
from tools.scraper.scraper.spiders.html_shopee import HtmlShopeeSpider
from modules.crawler.handlers.extractor import ExtractorService
from modules.crawler.models.model_category import Category
from modules.crawler.models.model_parser import ParserWaitUntil
from django.utils.translation import gettext_lazy as _

class Spider(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=256)
    url = models.CharField("URL", max_length=512)
    is_using_proxy = models.BooleanField("Using Proxy", default=False)
    class_parent = models.CharField("Class Parent", max_length=256, blank=True)
    class_child = models.CharField("Class Child", max_length=256, blank=True)
    limit_per_request = models.IntegerField("Limit per page", default=30)
    start_page = models.IntegerField("Start page", default=0)
    end_page = models.IntegerField("End page", default=100)
    base_url_item = models.CharField(
        "Base url item", default="", max_length=256, blank=True
    ) 
    is_headless = models.BooleanField("Not using browser", default=True, editable=True)
    domain = models.CharField("Domain", default="", max_length=256)
    agency = models.CharField("Agency", default="", max_length=256)
    parser_wait_until_parent = models.ForeignKey(ParserWaitUntil, on_delete=models.CASCADE, editable=True, null=True, blank=True, related_name='spirder_parser_parent')
    parser_wait_until_child = models.ForeignKey(ParserWaitUntil, on_delete=models.CASCADE, editable=True, null=True, blank=True, related_name='spirder_parser_child')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_running = models.BooleanField("Is running", default=False, editable=False)

    def __str__(self):
        return self.name


class Scraper(models.Model):
    class ScraperType(models.TextChoices):
        API = "api", _("API")
        HTML = "html", _("HTML")
        HTML_SHOPEE = "html_shopee", _("HTML_SHOPEE")

    class SchedulerType(models.TextChoices):
        ONCE = "once", _("Once")
        HOURLY = "hourly", _("Hourly")
        DAILY = "daily", _("Daily")
        # WEEKLY = 'weekly', _('Weekly')
        # MONTHLY = 'month', _('Monthly')
        # YEARLY = 'yearly', _('Yearly')

    class CrawlType(models.TextChoices):
        ALL = "all", _("All")
        LATEST = "latest", _("Latest")

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=256)
    homepage = models.CharField(max_length=256)

    scraper_type = models.CharField(
        max_length=50, choices=ScraperType.choices, default=ScraperType.API
    )
    crawl_type = models.CharField(
        max_length=50, choices=CrawlType.choices, default=CrawlType.LATEST
    )
    scheduler_type = models.CharField(
        max_length=50, choices=SchedulerType.choices, default=SchedulerType.ONCE
    )
    start_time = models.TimeField()
    start_date = models.DateField()
    job_id = models.CharField(max_length=256)
    is_active = models.BooleanField("Active", default=False)
    spiders = models.ManyToManyField(Spider, through="ScraperSpider")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def start_crawling(self):
        if self.is_active is False:
            return

        configure_logging()
        crawl_settings = Settings()
        crawl_settings.setmodule("tools.scraper.scraper.settings")

        for _spider in self.scraperspider_set.all():
            spider_db = _spider.spider
            params = {}
            if spider_db.is_headless:
                params["SELENIUM_DRIVER_ARGUMENTS"] = ['--headless']
            else: params["SELENIUM_DRIVER_ARGUMENTS"] = []
            crawl_settings.update(params)
            runner = CrawlerRunner(crawl_settings)
            
            spider_db.is_running = True
            spider_db.save()
            if self.scraper_type == "api":
                runner.crawl(ApiSpider, spider=_spider)
            if self.scraper_type == "html":
                runner.crawl(HtmlSpider, spider=_spider)
            if self.scraper_type == "html_shopee":
                runner.crawl(HtmlShopeeSpider, spider=_spider)

    def update_job(self):
        if self.job_id is not None:
            try:
                scheduler.remove_job(job_id=self.job_id)
            except JobLookupError:
                print("No job")

        job_id = None
        if self.scheduler_type == "once":
            job_id = scheduler.add_job(
                self.start_crawling,
                trigger="date",
                run_date="{} {}".format(self.start_date, self.start_time),
            ).id

        if self.scheduler_type == "hourly":
            job_id = scheduler.add_job(
                self.start_crawling,
                trigger="cron",
                args=[self],
                minute=self.start_time.minute,
            ).id

        if self.scheduler_type == "daily":
            job_id = scheduler.add_job(
                self.start_crawling,
                trigger="cron",
                minute=self.start_time.minute,
                hour=self.start_time.hour,
            ).id

        self.job_id = job_id

    def __str__(self):
        return self.name


class ScraperSpider(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    scraper = models.ForeignKey(Scraper, on_delete=models.CASCADE)
    spider = models.ForeignKey(Spider, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.spider.name, self.spider.is_running)

