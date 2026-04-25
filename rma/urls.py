from django.urls import path

from . import views

app_name = "rma"

urlpatterns = [
    path("", views.rma_list, name="rma_list"),
    path("new/", views.rma_create, name="rma_create"),
    path("<int:pk>/", views.rma_detail, name="rma_detail"),
]
