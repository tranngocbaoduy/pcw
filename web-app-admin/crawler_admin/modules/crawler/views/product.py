import base64
import uuid
import random 

from decimal import Decimal
from datetime import datetime
from modules.crawler.models.product import Product
from modules.crawler.serializers.product import ProductSerializer, ProductSerializerDetail
from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.core.files.base import ContentFile 
from django.db.models.functions import StrIndex
from django.db import models
from django.db.models import Func
import itertools

class Position(Func):
    function = 'POSITION'
    arg_joiner = ' IN '

    def __init__(self, expression, substring):
        super(Position, self).__init__(substring, expression)
 
def get_combination_words(sentence):
    words = sentence.split(' ')
    len_words = len(words)
    if len_words > 2:
        result = [] 
        for n in range(2, len_words):
            for res in itertools.combinations(words, n):
                result.append(" ".join(res))  
        result.reverse() 
        return result
    else:
        return words

class ProductView(APIView):
    def get(self, request, pk=None, category=None):

        min_price = request.query_params.get('min', 1) 
        discount = request.query_params.get('discount', 0) 
        max_price = request.query_params.get('max', 10000000000) 
        limit = request.query_params.get('limit', 20) 
        page = request.query_params.get('page', 1) 
        quantity = int(limit) * int(page) 
        from_quantity = int(limit) * (int(page) -1) 
        agency = request.query_params.get('agency', '') 
        search_string = request.query_params.get('q', '')  
        search_string_for_category = request.query_params.get('query', '')  
        
        random.seed(2608)
        products = []    
        if search_string: 
            if agency:
                agencies = agency.split(",")
                for agent in agencies:
                    for key_word in get_combination_words(search_string):
                        ids_map = list(map(lambda x: x.id, products)) 
                        items = (
                            Product.objects
                            .filter(
                                title__icontains=key_word, 
                                price__gte=min_price,
                                base_url__icontains=agent,
                                price__lte=max_price,
                                is_subscribe=True
                            )
                            .annotate(pos=Position('title', models.Value(key_word)))
                            .exclude(id__in=ids_map)
                            .order_by('-pos')
                        ) 
                        products.extend(items) 
             
                random.shuffle(products)
                serializer = ProductSerializer(products[from_quantity:quantity], many=True)
                return Response({"products": serializer.data})
                
            
            for key_word in get_combination_words(search_string):
                ids_map = list(map(lambda x: x.id, products)) 
                items = (
                    Product.objects
                    .filter(
                        title__icontains=key_word, 
                        price__gte=min_price,
                        price__lte=max_price,
                        is_subscribe=True
                    )
                    .annotate(pos=Position('title', models.Value(key_word)))
                    .exclude(id__in=ids_map)
                    .order_by('-pos')
                )
                products.extend(items)  
            
            random.shuffle(products)
            serializer = ProductSerializer(products[from_quantity:quantity], many=True)
            return Response({"products": serializer.data})
        
        if discount:
            products = Product.objects.filter(discount_rate__lte=discount,discount_rate__gte=0,is_subscribe=True)
            serializer = ProductSerializer(products[from_quantity:quantity], many=True)
            return Response({"products": serializer.data})

        if category == '':
            return Response({"products": []}) 

        if pk: 
            product = get_object_or_404(Product.objects.filter(category__id=category), pk=pk)
            serializer = ProductSerializerDetail(product)
            return Response({"product": serializer.data})

        if search_string_for_category:
            if agency:
                agencies = agency.split(",") 
                for agent in agencies:
                    for key_word in get_combination_words(search_string_for_category):
                        ids_map = list(map(lambda x: x.id, products))
                        items = (
                            Product.objects
                            .filter(
                                category__id=category,
                                title__icontains=key_word, 
                                price__gte=min_price,
                                base_url__icontains=agent,
                                price__lte=max_price,
                                is_subscribe=True
                            )
                            .annotate(pos=Position('title', models.Value(key_word)))
                            .exclude(id__in=ids_map)
                            .order_by('-pos')
                        )
                        products.extend(items)

                random.shuffle(products)
                serializer = ProductSerializer(products[from_quantity:quantity], many=True)
                return Response({"products": serializer.data})
            
            for key_word in get_combination_words(search_string_for_category):
                ids_map = list(map(lambda x: x.id, products)) 
                items = (
                    Product.objects
                    .filter(
                        category__id=category,
                        title__icontains=key_word, 
                        price__gte=min_price,
                        price__lte=max_price,
                        is_subscribe=True
                    )
                    .annotate(pos=Position('title', models.Value(key_word)))
                    .exclude(id__in=ids_map)
                    .order_by('-pos')
                )
                products.extend(items)  
            
            serializer = ProductSerializer(products[from_quantity:quantity], many=True)
            return Response({"products": serializer.data})

        if agency:
            agencies = agency.split(",") 
            for agent in agencies:
                items = Product.objects.filter(category__id=category,base_url__icontains=agent,price__gte=min_price,price__lte=max_price,is_subscribe=True)
                products.extend(items) 
        
            random.shuffle(products)
            serializer = ProductSerializer(products[from_quantity:quantity], many=True)
            return Response({"products": serializer.data})
         
        products = Product.objects.filter(category__id=category, price__gte=min_price,price__lte=max_price,is_subscribe=True)
        serializer = ProductSerializer(products[from_quantity:quantity], many=True)
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

