from modules.crawler.models.product import Category
from modules.crawler.serializers.product import CategorySerializer  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404 
from modules.crawler.views.types import EN_2_VN_CATEGORY

class CategoryView(APIView):
 
    def get_all_last_child_node(self):
        all_root_category = Category.objects.filter(parent=None) 
        sub_categories = []
        for category in all_root_category: sub_categories.extend(category.get_leafnodes())
        return sub_categories

    def get(self, request, pk=None):
        limit = request.query_params.get('limit', 20) 
        page = request.query_params.get('page', 1) 
        quantity = int(limit) * int(page) 
        from_quantity = int(limit) * (int(page) -1) 

        action = request.query_params.get('action', 1) 
        
        # if action:
        #     if action == 'top': 
        #         serializer = CategorySerializer(self.get_all_last_child_node(), many=True)
        #         return Response({"categories": serializer.data})
         
        if pk: 
            category = get_object_or_404(Category.objects.all(), pk=pk)
            serializer = CategorySerializer(category)
            return Response({"category": serializer.data})
         
        categories = Category.objects.all()
        serializer = CategorySerializer(categories[from_quantity:quantity], many=True)
        return Response({"categories": serializer.data})
 