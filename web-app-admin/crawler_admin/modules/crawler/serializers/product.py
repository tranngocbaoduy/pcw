from rest_framework import serializers
from modules.crawler.models.product import Product, GroupProduct, Category

class CategorySerializer(serializers.ModelSerializer):

    parent_categories = serializers.SerializerMethodField(
        read_only=True, method_name="get_parent_categories")

    is_leaf = serializers.SerializerMethodField(read_only=True, method_name="get_is_leaf")

    class Meta:
        model = Category
        read_only = ('is_root')
        fields = [
            'id',
            'name', 
            'parent_categories', 
            'is_leaf'
        ]

    def get_is_leaf(self, obj): 
        return True if obj.is_leaf_node() else False

    def get_parent_categories(self, obj):
        """ self referral field """ 
        ancestors = obj.get_ancestors() 
        serializer = CategorySerializer(
            instance=ancestors,
            many=True
        )
        return serializer.data

class GroupProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupProduct
        fields = [  "id","name", "description", "list_image", "meta"]

class ProductSerializer(serializers.ModelSerializer): 

    store_name = serializers.SerializerMethodField(read_only=True, method_name="get_store_name")
    largest_price = serializers.SerializerMethodField(read_only=True, method_name="get_largest_price")
    smallest_price = serializers.SerializerMethodField(read_only=True, method_name="get_smallest_price")

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
            "store_name",
            "largest_price",
            "smallest_price",
            # "meta",
            "price",
            "tags",
            "list_image",
            "list_price",
            "is_used",
            "updated_at",
            "last_updated_price"
        ]

    def get_store_name(self, obj):
        return obj.group_product.store_name

    def get_smallest_price(self,obj):
        return obj.group_product.smallest_price

    def get_largest_price(self,obj):
        return obj.group_product.largest_price


class ProductSerializerDetail(serializers.ModelSerializer):
    group_product = GroupProductSerializer()
    category = CategorySerializer()
    store_name = serializers.SerializerMethodField(read_only=True, method_name="get_store_name")

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
            "store_name",
            "price",
            "list_price",
            "updated_at",
        ]

    def get_store_name(self, obj):
        return obj.group_product.store_name