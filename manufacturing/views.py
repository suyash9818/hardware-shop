from django.shortcuts import render

from .models import ManufacturingOrder


def dashboard(request):
    open_orders = ManufacturingOrder.objects.exclude(status__in=["COMPLETED", "CANCELLED"]).order_by("-created_at")[:50]
    return render(request, "manufacturing/dashboard.html", {"open_orders": open_orders})
