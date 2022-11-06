from rest_framework import serializers
from modules.crawler.models.model_product import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "clean_name",
            "url",
            "base_encoded_url",
            "domain",
            "agency",
            "product_code",
            "category",
            "brand",
            "group_product",
            "seller",
            "slug_id",
            "image",
            "description",
            "stock",
            "price",
            "list_price",
            "updated_at",
        ]
