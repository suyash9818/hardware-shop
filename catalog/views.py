from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Compatibility, Product


def home(request):
    return render(request, "home_clean.html")


def product_list(request):
    products = Product.objects.select_related("category").all()
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
