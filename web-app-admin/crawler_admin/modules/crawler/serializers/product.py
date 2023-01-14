from rest_framework import serializers
from modules.crawler.models.product import Product, GroupProduct, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [  "id","name", ]

class GroupProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupProduct
        fields = [  "id","name", "description", "list_image", "meta"]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name", 
            "title",
            "base_url",
            "encoded_base_url", 
            "category",
            "discount_rate",
            "group_product",  
            "price",
            "list_image",
            "list_price",
            "updated_at",
        ]


class ProductSerializerDetail(serializers.ModelSerializer):
    group_product = GroupProductSerializer()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            "id",
            "name", 
            "title",
            "base_url",
            "encoded_base_url", 
            "category",  
            "list_image",
            "group_product", 
            "price",
            "list_price",
            "updated_at",
        ]
