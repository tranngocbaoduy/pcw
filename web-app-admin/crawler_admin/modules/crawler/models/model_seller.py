import uuid
from django.db import models
from modules.crawler.models.model_category import Category


class Seller(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=256, blank=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    review = models.IntegerField(default=0, null=True)
    star = models.FloatField(default=0, blank=True, null=True)
    image = models.CharField(max_length=256, blank=True, null=True)
    agency = models.CharField(max_length=256, blank=True)
    url = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.agency)
