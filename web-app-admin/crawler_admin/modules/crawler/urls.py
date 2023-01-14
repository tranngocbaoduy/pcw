from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from modules.crawler.views.product import ProductView
from modules.crawler.views.group import GroupProductView
from modules.crawler.views.category import CategoryView



urlpatterns = [
    path("api/products/search", ProductView.as_view()),
    path("api/products/<str:category>", ProductView.as_view()),
    path("api/products/<str:category>/<str:pk>", ProductView.as_view()),

    path("api/groups", GroupProductView.as_view()),
    path("api/groups/<str:pk>", GroupProductView.as_view()),

    path("api/categories", CategoryView.as_view()),
    path("api/categories/<str:pk>", CategoryView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
