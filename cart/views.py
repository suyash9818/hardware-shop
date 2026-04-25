from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Cart, CartItem
from catalog.models import Product
from orders.models import Order, OrderItem


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
    items = CartItem.objects.filter(cart=cart).select_related("product") if cart else CartItem.objects.none()
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, "cart/cart.html", {"items": items, "total": total})


@require_POST
def checkout(request):
    cart = get_cart(request, create=False)
    if not cart:
        return redirect("cart:view_cart")
    
    items = CartItem.objects.filter(cart=cart).select_related("product")
    if not items.exists():
        return redirect("cart:view_cart")
    
    order = Order.objects.create(status=Order.Status.DRAFT)
    
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            unit_price_usd=item.product.price_usd,
        )
    
    items.delete()
    return redirect("orders:order_quote", order_id=order.id)
