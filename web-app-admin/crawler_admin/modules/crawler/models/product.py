import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from modules.crawler.models.utils import id_generator, id_gen

class Category(models.Model): 

    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
    ) 
    name = models.CharField(max_length=256) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '#C{} - {}'.format(self.id, self.name)

class GroupProduct(models.Model):
    id = models.CharField(
        primary_key=True, default=id_generator, editable=False, unique=True, max_length=12
    )
    name = models.CharField(max_length=256)
    description = models.TextField(default="", blank=True,)
    list_image = models.TextField(default="", blank=True,)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model): 

    id = models.CharField(
        primary_key=True, default=id_generator, editable=False, unique=True, max_length=12
    )
    base_url = models.CharField(max_length=512, default='')
    name = models.CharField(max_length=512)
    title = models.CharField(max_length=512)
    encoded_base_url = models.CharField(max_length=512) 
    price = models.CharField(max_length=100,default="",blank=True,)
    list_price = models.CharField(max_length=100,default="",blank=True,)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    group_product = models.ForeignKey(GroupProduct, on_delete=models.CASCADE, blank=True, null=True)

    meta = models.JSONField(default=dict) 
    description = models.TextField(default="", blank=True,)
    list_image = models.TextField(default="", blank=True,)

    count_update = models.IntegerField("Count Update", default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '#P{} - {}'.format(self.id, self.name)