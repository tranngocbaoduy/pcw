import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class ParserWaitUntil(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    class SelectorType(models.TextChoices):
        XPATH = "xpath", _("XPATH")
        CSS = "css", _("CSS")

    name = models.CharField(max_length=256)
    selector_type = models.CharField(
        max_length=50, choices=SelectorType.choices, default=SelectorType.XPATH
    )
    selector = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Parser(models.Model):
    from modules.crawler.models.model_spider import Spider

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    class SelectorType(models.TextChoices):
        XPATH = "xpath", _("XPATH")
        CSS = "css", _("CSS")

    name = models.CharField(max_length=256)
    selector_type = models.CharField(
        max_length=50, choices=SelectorType.choices, default=SelectorType.XPATH
    )
    selector = models.CharField(max_length=256)
    spider = models.ForeignKey(Spider, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
