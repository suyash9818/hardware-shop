from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.order_list, name="order_list"),
    path("create/<int:product_id>/", views.create_order_for_product, name="create_order_from_product"),
    path("<int:order_id>/", views.order_detail, name="order_detail"),
    path("<int:order_id>/submit/", views.order_submit, name="order_submit"),
    path("<int:order_id>/quote/", views.order_quote, name="order_quote"),
]
