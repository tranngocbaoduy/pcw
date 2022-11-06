from modules.crawler.models.utils import id_gen
from django.db import models
from modules.crawler.models.model_category import Category
from django.contrib.postgres.fields import ArrayField


class GroupProduct(models.Model):
    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
    )
    name = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    agencies = ArrayField(
        ArrayField(
            models.CharField(max_length=10, blank=True),
            size=10,
            blank=True,
        ),
        size=100,
        default=list,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)
