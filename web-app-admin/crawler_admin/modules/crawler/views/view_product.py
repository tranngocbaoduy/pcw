import base64
import uuid
from datetime import datetime 
from modules.crawler.models.model_product import Product
from modules.crawler.serializers.serializer_product import ProductSerializer 
from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404  
from django.core.files.base import ContentFile

class ProductView(APIView):

    def get(self, request, pk=None): 
        if pk:
            product = get_object_or_404(Product.objects.all(), pk=pk) 
            serializer = ProductSerializer(product)
            return Response({"product": serializer.data})
            
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"products": serializer.data})
    
    def post(self, request):
        product = request.data.get('product')  
        # Create an product from the above data
        serializer = ProductSerializer(data=product)
        if serializer.is_valid(raise_exception=True):
            product_saved = serializer.save()
        return Response({"success": "Product '{}' created successfully".format(product_saved.id)})

    def put(self, request, pk):
        saved_product = get_object_or_404(Product.objects.all(), pk=pk)
        data = request.data.get('product')
        serializer = ProductSerializer(instance=saved_product, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            product_saved = serializer.save()
        return Response({"success": "Product '{}' updated successfully".format(product_saved.id)})


    def delete(self, request, pk):
        # Get object with this pk
        product = get_object_or_404(Product.objects.all(), pk=pk)
        product.delete()
        return Response({"message": "Product with id `{}` has been deleted.".format(pk)},status=204)