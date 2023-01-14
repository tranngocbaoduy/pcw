from modules.crawler.models.product import Category
from modules.crawler.serializers.product import CategorySerializer  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404 
from modules.crawler.views.types import EN_2_VN_CATEGORY

class CategoryView(APIView):
    def get(self, request, pk=None):

        limit = request.query_params.get('limit', 20) 
        page = request.query_params.get('page', 1) 
        quantity = int(limit) * int(page) 
        from_quantity = int(limit) * (int(page) -1) 
         
        if pk: 
            category = get_object_or_404(Category.objects.all(), pk=pk)
            serializer = CategorySerializer(category)
            return Response({"category": serializer.data})
         
        categories = Category.objects.all()
        serializer = CategorySerializer(categories[from_quantity:quantity], many=True)
        return Response({"categories": serializer.data})
 