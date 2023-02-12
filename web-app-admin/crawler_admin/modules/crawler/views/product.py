import base64
import uuid
import random 
import json
import time
import os

from django.db.models.functions import Length
from pprint import pprint
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
    return [sentence]
    # words = sentence.split(' ')
    # len_words = len(words)
    # if len_words > 2:
    #     result = [] 
    #     for n in range(2, len_words):
    #         for res in itertools.combinations(words, n):
    #             result.append(" ".join(res))  
    #     result.reverse() 
    #     return result
    # else:
    #     return words

class ProductView(APIView):

    def get_unique_product_by_group_name(self, products):
        group_name_maps = []
        final_products = []
        for p in products: 
            if p.group_product.name not in group_name_maps: 
                group_name_maps.append(p.group_product.name)
                final_products.append(p)
        return final_products

    def get(self, request, pk=None, category=None):

        start_time = time.time()
        discount = request.query_params.get('discount', 0) 
        limit = request.query_params.get('limit', 20) 
        page = request.query_params.get('page', 1) 
        quantity = int(limit) * int(page) 
        from_quantity = int(limit) * (int(page) -1) 
        search_string = request.query_params.get('q', '')  
        search_string_for_category = request.query_params.get('query', '')  

        min_price = request.query_params.get('min', 1) 
        max_price = request.query_params.get('max', 10000000000) 
        agency = request.query_params.get('agency', '') 
        type_device = request.query_params.get('type', '')  
        year = request.query_params.get('year', '')  
        screen_size = request.query_params.get('screen', '')  
        storage_size = request.query_params.get('storageSize', '')  
        gen_name = request.query_params.get('gen', '')  
        ram_size = request.query_params.get('ram', '')  
        core_num = request.query_params.get('coreNum', '')  
        network_support = request.query_params.get('networkSupport', '')  
        border_size = request.query_params.get('borderSize', '')  
        
        is_unique_product = True if request.query_params.get('isUnique', False) == 'true' else False 
        
        if request.query_params.get('isUsed', False) == 'True': is_used = { 'is_used': True}
        elif request.query_params.get('isUsed', False) == 'All': is_used = {}
        else: is_used = { 'is_used': False }
        
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
                                is_subscribe=True,
                                **is_used,
                            )
                            # .annotate(pos=Position('title', models.Value(key_word)))
                            .exclude(id__in=ids_map)
                            
                            # .order_by('-pos')
                        ) 
                        products.extend(items) 

                random.shuffle(products)
                products = list(sorted(products, key=lambda x: x.price, reverse= False))
                serializer = ProductSerializer(products[from_quantity:quantity], many=True)
                print("[INFO] Elapsed time: {} seconds -- {}".format((time.time() - start_time), os.path.realpath(__file__)))  # nopep8
                return Response({"products": serializer.data})
                
            
            for key_word in get_combination_words(search_string):
                ids_map = list(map(lambda x: x.id, products)) 
                items = (
                    Product.objects
                    .filter(
                        title__icontains=key_word, 
                        price__gte=min_price,
                        price__lte=max_price,
                        is_subscribe=True,
                        **is_used,
                    )
                    # .annotate(pos=Position('title', models.Value(key_word)))
                    .exclude(id__in=ids_map)
                    
                    # .order_by('-pos')
                )
                products.extend(items)  
            
            random.shuffle(products)
            products = self.get_unique_product_by_group_name(products) if is_unique_product else products
            products = list(sorted(products, key=lambda x: x.price, reverse= False))
            serializer = ProductSerializer(products[from_quantity:quantity], many=True)
            print("[INFO] Elapsed time: {} seconds -- {}".format((time.time() - start_time), os.path.realpath(__file__)))  # nopep8
            return Response({"products": serializer.data})
        
        if discount:
            if discount and category:
                products = Product.objects.filter(
                    category__id=category,
                    discount_rate__lte=discount,
                    discount_rate__gte=0,
                    is_subscribe=True,
                    **is_used,).order_by('-discount_rate')
            else:
                products = Product.objects.filter(
                    discount_rate__lte=discount,
                    discount_rate__gte=0,
                    is_subscribe=True,
                    **is_used,).order_by('-discount_rate')
            products = self.get_unique_product_by_group_name(products) if is_unique_product else products
            serializer = ProductSerializer(products[from_quantity:quantity], many=True)
            print("[INFO] Elapsed time: {} seconds -- {}".format((time.time() - start_time), os.path.realpath(__file__)))  # nopep8
            return Response({"products": serializer.data})

        if category == '':
            print("[INFO] Elapsed time: {} seconds -- {}".format((time.time() - start_time), os.path.realpath(__file__)))  # nopep8
            return Response({"products": []}) 

        if pk: 
            product = get_object_or_404(Product.objects.filter(category__id=category), pk=pk)
            serializer = ProductSerializerDetail(product)
            print("[INFO] Elapsed time: {} seconds -- {}".format((time.time() - start_time), os.path.realpath(__file__)))  # nopep8
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
                                is_subscribe=True,
                                **is_used,
                            )
                            # .annotate(pos=Position('title', models.Value(key_word)))
                            .exclude(id__in=ids_map)
                            
                            # .order_by('-pos')
                        )
                        products.extend(items)

                random.shuffle(products)
                products = list(sorted(products, key=lambda x: x.price, reverse= False))
                serializer = ProductSerializer(products[from_quantity:quantity], many=True)
                print("[INFO] Elapsed time: {} seconds -- {}".format((time.time() - start_time), os.path.realpath(__file__)))  # nopep8
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
                        is_subscribe=True,
                        **is_used,
                    )
                    # .annotate(pos=Position('title', models.Value(key_word)))
                    .exclude(id__in=ids_map)
                    
                    # .order_by('-pos')
                )
                products.extend(items)  
            
            products = list(sorted(products, key=lambda x: x.price, reverse= False))
            products = self.get_unique_product_by_group_name(products) if is_unique_product else products
            serializer = ProductSerializer(products[from_quantity:quantity], many=True)
            print("[INFO] Elapsed time: {} seconds -- {}".format((time.time() - start_time), os.path.realpath(__file__)))  # nopep8
            return Response({"products": serializer.data})

        if agency or type_device or year or screen_size or storage_size or gen_name or ram_size or core_num or network_support or border_size:
            filters = {
                "agency": agency,
                "type_device": type_device,
                "gen_name": gen_name,
                "year": year,
                "screen_size": screen_size,
                "storage_size": storage_size,
                "ram_size": ram_size,
                "core_num": core_num,
                "network_support": network_support,
                "border_size": border_size,
            } 
            first_key_has_value = 'type_device'
            for m, n in filters.items(): 
                first_key_has_value = m
                if n: break

            pprint(filters) 
            values = list(filter(None, list(filters.values())))
            for k, f in filters.items():
                temp_ids_map = []     
                if f in values: 
                    print(f, first_key_has_value)
                    for value_seacrh in f.split(','):
                        if k == first_key_has_value:   
                            if k == 'agency': filter_regex = { "base_url__icontains": value_seacrh }
                            else: filter_regex = { "group_product__name__icontains": value_seacrh + '#' } 
                            items = Product.objects.filter(
                                category__id=category, 
                                price__gte=min_price,
                                price__lte=max_price,
                                is_subscribe=True,
                                **is_used,
                                **filter_regex
                            )
                            products.extend(items)     
                        else:  
                            items = list(filter(lambda x: value_seacrh in x.group_product.name + '#', products))
                            ids_map = list(map(lambda x: x.id, items)) 
                            temp_ids_map.extend(ids_map)   
                    if k != first_key_has_value:
                        # Find product by many search conditions 
                        products = list(filter(lambda x: x.id in temp_ids_map, products))     

            random.shuffle(products)
            products = list(sorted(products, key=lambda x: x.price, reverse= False))
            products = self.get_unique_product_by_group_name(products) if is_unique_product else products
            serializer = ProductSerializer(products[from_quantity:quantity], many=True)
            print("[INFO] Elapsed time: {} seconds -- {}".format((time.time() - start_time), os.path.realpath(__file__)))  # nopep8
            return Response({"products": serializer.data})
         
        products = Product.objects.filter(
            category__id=category, 
            price__gte=min_price,
            price__lte=max_price,
            is_subscribe=True,
            **is_used,)
        
        products = self.get_unique_product_by_group_name(products) if is_unique_product else products
        serializer = ProductSerializer(products[from_quantity:quantity], many=True)
        print("[INFO] Elapsed time: {} seconds -- {}".format((time.time() - start_time), os.path.realpath(__file__)))  # nopep8
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

