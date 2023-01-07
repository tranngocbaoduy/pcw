from rest_framework import serializers
from modules.crawler.models.product import Product, GroupProduct, Category
 
class GroupProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupProduct
        fields = [ "id","name", "description", "list_image", "meta"]

class GroupProductSerializerDetail(serializers.ModelSerializer): 
    class Meta:
        model = GroupProduct
        fields = [ 
            "id",
            "name", 
            "description", 
            "list_image", 
            "meta", 
        ]
