from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from modules.crawler.views.view_product import ProductView

urlpatterns = [
    path("api/products/", ProductView.as_view()),
    path("api/products/<str:pk>", ProductView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
