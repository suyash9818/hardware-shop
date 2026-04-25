from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.view_cart, name="view_cart"),
    path("add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
]
