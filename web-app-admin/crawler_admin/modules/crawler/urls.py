from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from modules.crawler.views.product import ProductView
from modules.crawler.views.group import GroupProductView

urlpatterns = [
    path("api/products/<str:category>/", ProductView.as_view()),
    path("api/products/<str:category>/<str:pk>", ProductView.as_view()),

    path("api/groups/<str:category>", GroupProductView.as_view()),
    path("api/groups/<str:category>/<str:pk>", GroupProductView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
