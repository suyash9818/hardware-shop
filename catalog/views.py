from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, render

from .models import Compatibility, Product


def home(request):
    from inventory.models import SerialUnit, StockItem
    from manufacturing.models import ManufacturingOrder
    from orders.models import Order
    from pricing.models import ProcurementOrder, SupplierOffer
    from rma.models import RMA

    stats = [
        {
            "label": "Products",
            "value": Product.objects.count(),
            "icon": "bi-grid-3x3-gap",
            "url": "/catalog/products/",
            "tone": "blue",
        },
        {
            "label": "On Hand",
            "value": StockItem.objects.aggregate(total=Sum("quantity"))["total"] or 0,
            "icon": "bi-box-seam",
            "url": "/inventory/dashboard/",
            "tone": "teal",
        },
        {
            "label": "Open Orders",
            "value": Order.objects.exclude(status__in=[Order.Status.FULFILLED, Order.Status.CANCELLED]).count(),
            "icon": "bi-receipt",
            "url": "/orders/",
            "tone": "amber",
        },
        {
            "label": "Supplier Offers",
            "value": SupplierOffer.objects.count(),
            "icon": "bi-cash-coin",
            "url": "/pricing/dashboard/",
            "tone": "green",
        },
    ]

    context = {
        "stats": stats,
        "featured_products": Product.objects.select_related("category").order_by("-created_at")[:4],
        "recent_orders": Order.objects.order_by("-created_at")[:5],
        "open_mfg_count": ManufacturingOrder.objects.exclude(status__in=["COMPLETED", "CANCELLED"]).count(),
        "open_procurement_count": ProcurementOrder.objects.exclude(status__in=["RECEIVED", "CANCELLED"]).count(),
        "available_serial_units": SerialUnit.objects.filter(status=SerialUnit.Status.AVAILABLE).count(),
        "open_rma_count": RMA.objects.exclude(status__in=[RMA.Status.RESOLVED, RMA.Status.REJECTED]).count(),
    }
    return render(request, "home_clean.html", context)


def product_list(request):
    products = Product.objects.select_related(
        "category",
        "family",
        "thread",
        "head",
        "drive",
        "material",
        "feature",
        "finish",
    ).all()
    query = request.GET.get("q")
    if query:
        products = products.filter(Q(name__icontains=query) | Q(specs__icontains=query) | Q(sku__icontains=query))
    return render(request, "catalog/product_list.html", {"products": products, "query": query or ""})


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
    compatible_products = get_compatible_products(product)
    return render(
        request,
        "catalog/product_detail.html",
        {"product": product, "compatible_products": compatible_products},
    )


def get_compatible_products(product):
    specs = product.specs or {}
    explicit_ids = list(
        Compatibility.objects.filter(product=product).values_list("compatible_product_id", flat=True)
    )
    candidates = Product.objects.exclude(id=product.id)
    compatible_ids = set(explicit_ids)
    for candidate in candidates:
        candidate_specs = candidate.specs or {}
        if specs.get("thread") and specs.get("thread") == candidate_specs.get("thread"):
            compatible_ids.add(candidate.id)
        elif specs.get("voltage") and specs.get("voltage") == candidate_specs.get("voltage"):
            compatible_ids.add(candidate.id)
    return Product.objects.filter(id__in=compatible_ids).order_by("name")


def search_products(request):
    return product_list(request)
