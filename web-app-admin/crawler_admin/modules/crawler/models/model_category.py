from modules.crawler.models.utils import id_gen
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.db import models

class Category(MPTTModel):
    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
    )
    name = models.CharField(max_length=250)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    vi_name = models.CharField(max_length=250, default='', blank=True, null=True)
    en_name = models.CharField(max_length=250, default='', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def group_product_by_code(self):
        list_product = Product.objects.filter(category=self.id)
        list_product_code = [product.product_code for product in list_product]
        stat = self.handle_stat_group(list_product_code)
        for name, quantity in stat.items():
            info_group_product = {
                "category": self,
                "name": name,
            }
            info_group_product, created = GroupProduct.objects.get_or_create(
                **info_group_product
            )
            if not created:
                # print({"message":'[UPDATE BRAND]', "info_brand": model_to_dict(info_brand)})
                for attr, value in model_to_dict(info_brand).items():
                    if attr == "category":
                        setattr(info_brand, attr, self)
                    else:
                        setattr(info_brand, attr, value)
                info_brand.save()
        print("[GROUP {} PRODUCT ITEMS]".format(len(list_product)), stat)

    def handle_stat_group(self, texts):
        stat_group = {}
        for i in texts:
            if i not in stat_group:
                stat_group[i] = 1
            else:
                stat_group[i] += 1
        return stat_group