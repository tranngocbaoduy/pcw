import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from modules.crawler.models.utils import id_gen


class WareParser(models.Model): 

    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
    ) 

    name = models.CharField(max_length=256) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Parser(models.Model): 

    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
    )

    class SelectorType(models.TextChoices):
        XPATH = "xpath", _("XPATH")
        CSS = "css", _("CSS")

    name = models.CharField(max_length=256)
    selector_type = models.CharField(
        max_length=50, choices=SelectorType.choices, default=SelectorType.XPATH
    )
    selector = models.CharField(max_length=256)
    spider = models.ForeignKey(WareParser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
