from django.shortcuts import render
from django.db.models import Sum, Count

from .models import StockItem, SerialUnit

def dashboard(request):
    low_stock = StockItem.objects.order_by("quantity")[:20]
    serialized_count = StockItem.objects.filter(is_serialized=True).count()
    serial_units_total = SerialUnit.objects.count()
    available_serial_units = SerialUnit.objects.filter(status="AVAILABLE").count()
    context = {
        "low_stock": low_stock,
        "serialized_count": serialized_count,
        "serial_units_total": serial_units_total,
        "available_serial_units": available_serial_units,
    }
    return render(request, "inventory/dashboard.html", context)
