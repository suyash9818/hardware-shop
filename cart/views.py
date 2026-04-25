from django.shortcuts import render, redirect, get_object_or_404

from .models import Cart, CartItem
from catalog.models import Product


def get_cart(request, create=True):
    if not request.session.session_key:
        if not create:
            return None
        request.session.create()

    cart, created = Cart.objects.get_or_create(session_id=request.session.session_key)
    return cart


def add_to_cart(request, pk):
    cart = get_cart(request)
    product = get_object_or_404(Product, pk=pk)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        item.quantity = 1
    else:
        item.quantity += 1
    item.save()
    return redirect("cart:view_cart")


def view_cart(request):
    cart = get_cart(request, create=False)
    items = CartItem.objects.filter(cart=cart) if cart else CartItem.objects.none()
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, "cart/cart.html", {"items": items, "total": total})
