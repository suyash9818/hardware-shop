from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Product
from hardware_shop.integrations.payments import StripePaymentGateway
from hardware_shop.integrations.shipping import ShippingGateway
from hardware_shop.integrations.tax import TaxGateway
from .models import Order, OrderItem
from .services import submit_order


def order_list(request):
    orders = Order.objects.order_by("-created_at")[:50]
    return render(request, "orders/order_list.html", {"orders": orders})


@require_POST
def create_order_for_product(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get("quantity", "1") or "1")
    qty = max(qty, 1)

    order = Order.objects.create(status=Order.Status.DRAFT)
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=qty,
        unit_price_usd=product.price_usd,
    )
    return redirect("orders:order_detail", order_id=order.id)


def order_detail(request, order_id: int):
    order = get_object_or_404(Order.objects.prefetch_related("items", "items__product"), id=order_id)
    return render(request, "orders/order_detail_clean.html", {"order": order})


@require_POST
def order_submit(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    auto = request.POST.get("auto_trigger_manufacturing", "1") == "1"
    submit_order(order, auto_trigger_manufacturing=auto)
    return redirect("orders:order_detail", order_id=order.id)


def order_quote(request, order_id: int):
    order = get_object_or_404(Order.objects.prefetch_related("items", "items__product"), id=order_id)
    subtotal = Decimal(order.total_usd)
    shipping_gateway = ShippingGateway()
    tax_gateway = TaxGateway()
    payment_gateway = StripePaymentGateway()

    state = request.GET.get("state", "CA")
    to_zip = request.GET.get("zip", "92831")
    weight_oz = float(max(order.items.count(), 1) * 16)
    rates = shipping_gateway.get_rates(to_zip=to_zip, weight_oz=weight_oz)
    selected_rate = rates[0] if rates else None
    shipping_amount = Decimal(str(selected_rate.amount_usd)) if selected_rate else Decimal("0.00")
    tax_amount = Decimal(str(tax_gateway.estimate_tax(float(subtotal + shipping_amount), state)))
    grand_total = subtotal + shipping_amount + tax_amount
    session = payment_gateway.create_checkout_session(order_id=order.id, amount_usd_cents=int(grand_total * 100))

    context = {
        "order": order,
        "subtotal": subtotal,
        "shipping_rates": rates,
        "selected_rate": selected_rate,
        "shipping_amount": shipping_amount,
        "state": state,
        "zip_code": to_zip,
        "tax_amount": tax_amount,
        "grand_total": grand_total,
        "payment_session": session,
        "payment_configured": payment_gateway.is_configured(),
        "shipping_configured": shipping_gateway.is_configured(),
        "tax_configured": tax_gateway.is_configured(),
    }
    return render(request, "orders/order_quote.html", context)
