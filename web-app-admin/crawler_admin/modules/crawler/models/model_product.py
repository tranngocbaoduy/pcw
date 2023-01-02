from modules.crawler.models.utils import id_gen
from django.utils.translation import gettext_lazy as _
from django.db import models
from modules.crawler.models.model_category import Category
from modules.crawler.models.model_brand import Brand
from modules.crawler.models.model_raw_product import RawProduct
from modules.crawler.models.model_group_product import GroupProduct
from modules.crawler.models.model_seller import Seller


class Product(models.Model):
    class ScraperType(models.TextChoices):
        API = "api", _("API")
        HTML = "html", _("HTML")
        HTML_SHOPEE = "html_shopee", _("HTML_SHOPEE")

    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
    )
    name = models.CharField("Name", max_length=256)
    clean_name = models.CharField("Clean Name", max_length=512)
    clean_slug_name = models.CharField("Clean Slug Name", max_length=512, default='')
    url = models.CharField("URL", max_length=512)
    base_encoded_url = models.CharField("Encode URL", max_length=512)
    domain = models.CharField("Domain", max_length=256)
    agency = models.CharField("Agency", max_length=256)
    product_code = models.CharField("Code", max_length=256)
    scraper_type = models.CharField(
        max_length=50, choices=ScraperType.choices, default=ScraperType.API
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    brand = models.CharField("Brand", default='', max_length=256)
    id_raw_product = models.ForeignKey(
        RawProduct, blank=True, null=True, on_delete=models.CASCADE
    )
    group_product = models.ForeignKey(
        GroupProduct, blank=True, null=True, on_delete=models.CASCADE
    )
    # seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    count_update = models.IntegerField("Count Update", default=0)

    slug_id = models.CharField("Slug Id", max_length=1024, blank=True)
    image = models.TextField(
        default="",
        blank=True,
    )
    # item_rating = models.TextField(
    #     default="",
    #     blank=True,
    # )
    description = models.TextField(
        default="",
        blank=True,
    )

    # stock = models.CharField(
    #     max_length=100,
    #     default="",
    #     blank=True,
    # )
    # historical_sold = models.CharField(
    #     max_length=100,
    #     default="",
    #     blank=True,
    # )
    # liked_count = models.CharField(
    #     max_length=100,
    #     default="",
    #     blank=True,
    # )
    price = models.CharField(
        max_length=100,
        default="",
        blank=True,
    )
    list_price = models.CharField(
        max_length=100,
        default="",
        blank=True,
    )

    score = models.CharField(
        max_length=100,
        default="",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
