from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Product
from orders.models import Order
from .forms import RMAForm
from .models import RMA


def rma_list(request):
    rmas = RMA.objects.select_related("product", "order", "serial_unit")[:100]
    return render(request, "rma/rma_list.html", {"rmas": rmas})


def rma_detail(request, pk: int):
    rma = get_object_or_404(RMA.objects.select_related("product", "order", "serial_unit"), pk=pk)
    return render(request, "rma/rma_detail.html", {"rma": rma})


def rma_create(request):
    initial = {}
    order_id = request.GET.get("order")
    product_id = request.GET.get("product")
    if order_id:
        initial["order"] = Order.objects.filter(pk=order_id).first()
    if product_id:
        initial["product"] = Product.objects.filter(pk=product_id).first()

    if request.method == "POST":
        form = RMAForm(request.POST)
        if form.is_valid():
            rma = form.save()
            messages.success(request, f"RMA #{rma.id} created successfully.")
            return redirect("rma:rma_detail", pk=rma.pk)
    else:
        form = RMAForm(initial=initial)
    return render(request, "rma/rma_form.html", {"form": form})
