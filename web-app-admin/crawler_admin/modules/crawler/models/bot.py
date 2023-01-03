import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from modules.crawler.models.utils import id_gen
from modules.crawler.models.sitemap import Sitemap
from apscheduler.jobstores.base import JobLookupError
from modules.crawler.apps import scheduler

from tools.scraper.scraper.spiders.html_headless import HtmlHeadless
from tools.scraper.scraper.spiders.html_non_headless import HtmlNonHeadless

from scrapy.settings import Settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

class Scraper(models.Model): 

    class SchedulerType(models.TextChoices):
        ONCE = "once", _("Once")
        HOURLY = "hourly", _("Hourly")
        DAILY = "daily", _("Daily")
        # WEEKLY = 'weekly', _('Weekly')
        # MONTHLY = 'month', _('Monthly')
        # YEARLY = 'yearly', _('Yearly') 

    id = models.CharField(
        primary_key=True, default=id_gen(6), editable=False, unique=True, max_length=12
    ) 

    name = models.CharField(max_length=256) 
    scheduler_type = models.CharField(
        max_length=50, choices=SchedulerType.choices, default=SchedulerType.ONCE
    )
    start_time = models.TimeField()
    start_date = models.DateField()
    job_id = models.CharField(max_length=256)
    is_active = models.BooleanField("Active", default=False)
    sitemap_cells = models.ManyToManyField(Sitemap, through="ScraperSitemap")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def start_crawling(self):
        if self.is_active is False:
            return

        configure_logging()
        crawl_settings = Settings()
        crawl_settings.setmodule("tools.scraper.scraper.settings")

        for _sitemap in self.scrapersitemap_set.all():
            _sitemap_db = _sitemap.sitemap
            params = {}
            print('_sitemap_db.crawl_type',_sitemap_db.crawl_type)
            if _sitemap_db.crawl_type == 'mpa':
                params["SELENIUM_DRIVER_ARGUMENTS"] = ["--headless"]
            else:
                params["SELENIUM_DRIVER_ARGUMENTS"] = []
            crawl_settings.update(params)
            runner = CrawlerRunner(crawl_settings) 
            _sitemap_db.save()   

            if _sitemap_db.crawl_type == 'mpa':
                runner.crawl(HtmlHeadless, url=_sitemap_db.base_url, spider=_sitemap_db)
            else:
                runner.crawl(HtmlNonHeadless, url=_sitemap_db.base_url, spider=_sitemap_db)

    def update_job(self):
        print('self.job_id',self.job_id)
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

        print('self.scheduler_type', {
            "scheduler_type":self.scheduler_type,
            "job_id":job_id,
        })
        self.job_id = job_id

    def __str__(self):
        return self.name


class ScraperSitemap(models.Model):
    
    id = models.CharField(
        primary_key=True, default=id_gen(6), editable=False, unique=True, max_length=12
    ) 
    scraper = models.ForeignKey(Scraper, on_delete=models.CASCADE)
    sitemap = models.ForeignKey(Sitemap, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "#{} - {}".format(self.sitemap.id,self.sitemap.name)
