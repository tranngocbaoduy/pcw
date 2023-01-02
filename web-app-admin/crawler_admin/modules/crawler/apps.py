from django.apps import AppConfig

from crochet import setup
from apscheduler.schedulers.background import BackgroundScheduler

# setup()
# scheduler = BackgroundScheduler()


class ScrapersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.crawler"

    # def ready(self):
    #     scheduler.start()
    #     import modules.crawler.signals
