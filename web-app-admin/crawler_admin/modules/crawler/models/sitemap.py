import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from modules.crawler.models.utils import id_gen


class Sitemap(models.Model): 

    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
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
