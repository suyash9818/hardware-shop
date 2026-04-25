from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from catalog.models import Category, Product
from hardware_shop.api.serializers import (
    CategorySerializer, CostAvailabilityProfileSerializer, ManufacturerSerializer, ManufacturingOrderSerializer,
    OrderSerializer, ProcurementOrderSerializer, ProductSerializer, RMASerializer, SerialUnitSerializer,
    StockItemSerializer, SupplierOfferSerializer, SupplierSerializer,
)
from inventory.models import SerialUnit, StockItem
from manufacturing.models import Manufacturer, ManufacturingOrder
from orders.models import Order
from orders.services import submit_order
from pricing.models import CostAvailabilityProfile, ProcurementOrder, Supplier, SupplierOffer
from rma.models import RMA


def api_docs(request):
    endpoints = [
        {"name": "Categories", "path": "/api/categories/", "methods": "GET, POST", "purpose": "List or create product categories."},
        {"name": "Products", "path": "/api/products/", "methods": "GET, POST", "purpose": "List or create products."},
        {"name": "Stock", "path": "/api/stock/", "methods": "GET, POST", "purpose": "List or create stock items."},
        {"name": "Serial Units", "path": "/api/serial-units/", "methods": "GET, POST", "purpose": "List or create serial-tracked units."},
        {"name": "Orders", "path": "/api/orders/", "methods": "GET, POST", "purpose": "List or create orders."},
        {"name": "Submit Order", "path": "/api/orders/{id}/submit/", "methods": "POST", "purpose": "Run fulfillment logic for an order."},
        {"name": "Manufacturers", "path": "/api/manufacturers/", "methods": "GET, POST", "purpose": "List or create manufacturers."},
        {"name": "Manufacturing Orders", "path": "/api/manufacturing-orders/", "methods": "GET, POST", "purpose": "List or create manufacturing orders."},
        {"name": "Suppliers", "path": "/api/suppliers/", "methods": "GET, POST", "purpose": "List or create suppliers."},
        {"name": "Supplier Offers", "path": "/api/supplier-offers/", "methods": "GET, POST", "purpose": "List or create supplier offers."},
        {"name": "Cost Profiles", "path": "/api/cost-profiles/", "methods": "GET, POST", "purpose": "List or create cost/availability profiles."},
        {"name": "Procurement Orders", "path": "/api/procurement-orders/", "methods": "GET, POST", "purpose": "List or create procurement orders."},
        {"name": "RMAs", "path": "/api/rmas/", "methods": "GET, POST", "purpose": "List or create warranty/RMA requests."},
        {"name": "JWT access token", "path": "/api/auth/token/", "methods": "POST", "purpose": "Issue JWT access and refresh tokens."},
        {"name": "JWT refresh", "path": "/api/auth/token/refresh/", "methods": "POST", "purpose": "Refresh a JWT access token."},
        {"name": "DRF auth token", "path": "/api/auth/token-auth/", "methods": "POST", "purpose": "Issue a DRF token."},
    ]
    return render(request, "api_docs.html", {"endpoints": endpoints})


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({"id": user.id, "username": user.username, "email": user.email})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class StockItemViewSet(viewsets.ModelViewSet):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer


class SerialUnitViewSet(viewsets.ModelViewSet):
    queryset = SerialUnit.objects.all()
    serializer_class = SerialUnitSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related("items")
    serializer_class = OrderSerializer

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        order = self.get_object()
        raw_auto = request.data.get("auto_trigger_manufacturing", True)
        if isinstance(raw_auto, bool):
            auto = raw_auto
        elif isinstance(raw_auto, str):
            auto = raw_auto.strip().lower() not in {"", "0", "false", "no", "off"}
        else:
            auto = bool(raw_auto)

        result = submit_order(order, auto_trigger_manufacturing=auto)
        order.refresh_from_db()
        payload = {"result": result, "order": OrderSerializer(order).data}
        return Response(payload)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplierOfferViewSet(viewsets.ModelViewSet):
    queryset = SupplierOffer.objects.all()
    serializer_class = SupplierOfferSerializer


class CostAvailabilityProfileViewSet(viewsets.ModelViewSet):
    queryset = CostAvailabilityProfile.objects.all()
    serializer_class = CostAvailabilityProfileSerializer


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class ManufacturingOrderViewSet(viewsets.ModelViewSet):
    queryset = ManufacturingOrder.objects.all()
    serializer_class = ManufacturingOrderSerializer


class ProcurementOrderViewSet(viewsets.ModelViewSet):
    queryset = ProcurementOrder.objects.all()
    serializer_class = ProcurementOrderSerializer


class RMAViewSet(viewsets.ModelViewSet):
    queryset = RMA.objects.all()
    serializer_class = RMASerializer
