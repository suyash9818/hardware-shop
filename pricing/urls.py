from django.urls import path
from . import views

app_name = "pricing"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
]
