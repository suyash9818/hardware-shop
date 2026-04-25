from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="catalog_home"),
    path("products/", views.product_list, name="product_list"),
    path("product/<int:pk>/", views.product_detail, name="product_detail_legacy"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("search/", views.search_products, name="search"),
]
