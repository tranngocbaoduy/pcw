import base64
import uuid

from datetime import datetime
from modules.crawler.models.product import GroupProduct, Product
from modules.crawler.serializers.group import GroupProductSerializer, GroupProductSerializerDetail
from modules.crawler.serializers.product import ProductSerializer
from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.core.files.base import ContentFile
from modules.crawler.views.types import EN_2_VN_CATEGORY

class GroupProductView(APIView):
    def get(self, request, pk=None, category=None):
    
        limit = request.query_params.get('limit', 20) 
        page = request.query_params.get('page', 1) 
        quantity = int(limit) * int(page) 
        from_quantity = int(limit) * (int(page) -1) 
        only_detail = request.query_params.get('only_detail', False) 
        category_id = request.query_params.get('category_id', '') 
        print('category_id',category_id)
        if category_id:
            groups = GroupProduct.objects.filter(category=category_id)
            filterWares = []
            for group in groups:
                if group.category.name == 'Macbook':
                    print('group.name',group.name)
                    kind, year, gen_name, screen_size, storage_size, ram_size, core_number, _ = group.name.split('#') 
                    data = {
                        "kind": kind, 
                        "gen": gen_name,
                        "year": year, 
                        "screen_size": screen_size,
                        "storage_size": storage_size,
                        "ram_size": ram_size,
                        "core_number": core_number
                    } 
                    if data not in filterWares: filterWares.append(data)
                elif group.category.name == 'Apple Watch': 
                    gen_name, size_number, network_support, border, _ = group.name.split('#') 
                    data = { 
                        "gen": gen_name,
                        "size_number": size_number, 
                        "network_support": network_support,
                        "border": border, 
                    } 
                    if data not in filterWares: filterWares.append(data)

                elif group.category.name == 'iPhone':
                    kind, storage_size, _ = group.name.split('#') 
                    data = {
                        "kind": kind, 
                        "storage_size": storage_size
                    }
                    if data not in filterWares: filterWares.append(data)

            if filterWares and len(filterWares) > 0:
                return Response({"data": filterWares})
            return Response({"data": {}})
  
        if pk:
            group = get_object_or_404(GroupProduct.objects.all(), pk=pk)
            serializer = GroupProductSerializerDetail(group)
           
            if only_detail:
                products = Product.objects.filter(group_product=group.id, is_subscribe=True).order_by('price')
                product_serializer = ProductSerializer(products, many=True)
                return Response({"group": serializer.data, "list_product":product_serializer.data})
            return Response({"group": serializer.data})


        groups = GroupProduct.objects.all()
        serializer = GroupProductSerializer(groups[from_quantity:quantity], many=True)
        return Response({"groups": serializer.data})

    # def post(self, request):
    #     group = request.data.get("group")
    #     # Create an group from the above data
    #     serializer = GroupProductSerializer(data=group)
    #     if serializer.is_valid(raise_exception=True):
    #         group_saved = serializer.save()
    #     return Response(
    #         {"success": "GroupProduct '{}' created successfully".format(group_saved.id)}
    #     )

    # def put(self, request, pk):
    #     instance = get_object_or_404(GroupProduct.objects.all(), pk=pk)
    #     data = request.data.get("group")
    #     serializer = GroupProductSerializer(instance=instance, data=data, partial=True)

    #     if serializer.is_valid(raise_exception=True):
    #         group_saved = serializer.save()
    #     return Response(
    #         {"success": "GroupProduct '{}' updated successfully".format(group_saved.id)}
    #     )

    # def delete(self, request, pk):
    #     # Get object with this pk
    #     group = get_object_or_404(GroupProduct.objects.all(), pk=pk)
    #     group.delete()
    #     return Response(
    #         {"message": "GroupProduct with id `{}` has been deleted.".format(pk)}, status=204
    #     )
