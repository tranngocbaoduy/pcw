from django import forms
from django.apps import apps
from django.forms import BaseInlineFormSet

# Create your forms here.
from modules.crawler.models.model_spider import Spider

class ParserInlineFormSet(BaseInlineFormSet):
    pass


class ProductInlineFormSet(BaseInlineFormSet):
    pass
