import base64
import uuid
import random 

from datetime import datetime
from modules.crawler.models.product import Product
from modules.crawler.serializers.product import ProductSerializer, ProductSerializerDetail
from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.core.files.base import ContentFile
from modules.crawler.views.types import EN_2_VN_CATEGORY

class ProductView(APIView):
    def get(self, request, pk=None, category=None):

        limit = request.query_params.get('limit', 20) 
        page = request.query_params.get('page', 1) 
        quantity = int(limit) * int(page)
        agency = request.query_params.get('agency', '') 
        
        if category == '' or category not in EN_2_VN_CATEGORY.keys(): 
            return Response({"products": []})
        category = EN_2_VN_CATEGORY[category]

        if pk: 
            product = get_object_or_404(Product.objects.filter(category__name=category), pk=pk)
            serializer = ProductSerializerDetail(product)
            return Response({"product": serializer.data})
        
        if agency:
            agencies = agency.split(",")
            products = [] 
            for agent in agencies:
                items = Product.objects.filter(category__name=category,base_url__contains=agent) 
                products.extend(items) 
        
            random.seed(26)
            random.shuffle(products)
            serializer = ProductSerializer(products[:quantity], many=True)
            return Response({"products": serializer.data})
            
        products = Product.objects.filter(category__name=category)
        serializer = ProductSerializer(products[:quantity], many=True)
        return Response({"products": serializer.data})

    # def post(self, request):
    #     product = request.data.get("product")
    #     # Create an product from the above data
    #     serializer = ProductSerializer(data=product)
    #     if serializer.is_valid(raise_exception=True):
    #         product_saved = serializer.save()
    #     return Response(
    #         {"success": "Product '{}' created successfully".format(product_saved.id)}
    #     )

    # def put(self, request, pk):
    #     instance = get_object_or_404(Product.objects.all(), pk=pk)
    #     data = request.data.get("product")
    #     serializer = ProductSerializer(instance=instance, data=data, partial=True)

    #     if serializer.is_valid(raise_exception=True):
    #         product_saved = serializer.save()
    #     return Response(
    #         {"success": "Product '{}' updated successfully".format(product_saved.id)}
    #     )

    # def delete(self, request, pk):
    #     # Get object with this pk
    #     product = get_object_or_404(Product.objects.all(), pk=pk)
    #     product.delete()
    #     return Response(
    #         {"message": "Product with id `{}` has been deleted.".format(pk)}, status=204
    #     )

