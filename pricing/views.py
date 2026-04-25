from django.shortcuts import render
from django.db.models import Min

from .models import SupplierOffer, ProcurementOrder

def dashboard(request):
    offers = SupplierOffer.objects.select_related("supplier", "product").order_by("product__sku", "purchase_cost_usd")[:200]
    # compute cheapest offer per product (simple)
    cheapest = {}
    for o in offers:
        if o.product_id not in cheapest:
            cheapest[o.product_id] = o
    procurements = ProcurementOrder.objects.select_related("supplier", "product").order_by("-created_at")[:50]
    return render(request, "pricing/dashboard_clean.html", {"offers": offers, "cheapest": cheapest, "procurements": procurements})
