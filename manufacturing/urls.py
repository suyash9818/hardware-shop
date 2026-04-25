from django.urls import path
from . import views

app_name = "manufacturing"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
]
