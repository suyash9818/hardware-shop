from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from catalog.models import Category, Product
from inventory.models import SerialUnit, StockItem
from pricing.models import CostAvailabilityProfile, Supplier, SupplierOffer, ProcurementOrder
from manufacturing.models import ManufacturingOrder
from .models import Order, OrderItem


class OrderModelAndViewTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Sensors", slug="sensors")
        self.product = Product.objects.create(
            sku="SNS-001",
            name="Proximity Sensor",
            category=category,
            price_usd=Decimal("14.50"),
            specs={"voltage": "24V"},
        )

    def test_order_total_usd_sums_all_line_items(self):
        order = Order.objects.create(status=Order.Status.DRAFT)
        OrderItem.objects.create(order=order, product=self.product, quantity=2, unit_price_usd=Decimal("14.50"))
        OrderItem.objects.create(order=order, product=self.product, quantity=1, unit_price_usd=Decimal("5.00"))
        self.assertEqual(order.total_usd, Decimal("34.00"))

    def test_create_order_for_product_route_creates_draft_order(self):
        response = self.client.post(reverse("orders:create_order_from_product", args=[self.product.id]), {"quantity": 3})
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get()
        item = order.items.get()
        self.assertEqual(order.status, Order.Status.DRAFT)
        self.assertEqual(item.quantity, 3)
        self.assertEqual(item.unit_price_usd, self.product.price_usd)

    def test_order_submit_uses_inventory_and_marks_order_fulfilled(self):
        StockItem.objects.create(product=self.product, warehouse="Main Warehouse", quantity=5, is_serialized=False)
        order = Order.objects.create(status=Order.Status.DRAFT)
        OrderItem.objects.create(order=order, product=self.product, quantity=2, unit_price_usd=self.product.price_usd)
        response = self.client.post(reverse("orders:order_submit", args=[order.id]), {"auto_trigger_manufacturing": "0"})
        order.refresh_from_db()
        stock_item = StockItem.objects.get(product=self.product)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.status, Order.Status.FULFILLED)
        self.assertIsNotNone(order.submitted_at)
        self.assertEqual(stock_item.quantity, 3)

    def test_order_submit_uses_supplier_when_inventory_missing(self):
        supplier = Supplier.objects.create(name="Acme Supply")
        SupplierOffer.objects.create(product=self.product, supplier=supplier, purchase_cost_usd=Decimal("8.00"), lead_time_days=4, min_order_qty=1, available_qty=10)
        order = Order.objects.create(status=Order.Status.DRAFT)
        OrderItem.objects.create(order=order, product=self.product, quantity=2, unit_price_usd=self.product.price_usd)
        self.client.post(reverse("orders:order_submit", args=[order.id]), {"auto_trigger_manufacturing": "1"})
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.IN_PRODUCTION)
        self.assertEqual(ProcurementOrder.objects.count(), 1)

    def test_order_submit_uses_manufacturing_when_no_inventory_or_supplier(self):
        CostAvailabilityProfile.objects.create(product=self.product, manufacturing_cost_usd=Decimal("6.50"), manufacturing_lead_time_days=5)
        order = Order.objects.create(status=Order.Status.DRAFT)
        OrderItem.objects.create(order=order, product=self.product, quantity=1, unit_price_usd=self.product.price_usd)
        self.client.post(reverse("orders:order_submit", args=[order.id]), {"auto_trigger_manufacturing": "1"})
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.IN_PRODUCTION)
        self.assertEqual(ManufacturingOrder.objects.count(), 1)

    def test_order_submit_ignores_supplier_offer_without_available_quantity(self):
        supplier = Supplier.objects.create(name="Unavailable Supply")
        SupplierOffer.objects.create(
            product=self.product,
            supplier=supplier,
            purchase_cost_usd=Decimal("4.00"),
            lead_time_days=2,
            min_order_qty=1,
            available_qty=0,
        )
        CostAvailabilityProfile.objects.create(
            product=self.product,
            manufacturing_cost_usd=Decimal("6.50"),
            manufacturing_lead_time_days=5,
        )
        order = Order.objects.create(status=Order.Status.DRAFT)
        OrderItem.objects.create(order=order, product=self.product, quantity=1, unit_price_usd=self.product.price_usd)

        self.client.post(reverse("orders:order_submit", args=[order.id]), {"auto_trigger_manufacturing": "1"})

        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.IN_PRODUCTION)
        self.assertEqual(ProcurementOrder.objects.count(), 0)
        self.assertEqual(ManufacturingOrder.objects.count(), 1)

    def test_order_submit_does_not_use_serialized_stock_without_enough_available_units(self):
        stock_item = StockItem.objects.create(
            product=self.product,
            warehouse="Serialized Warehouse",
            quantity=5,
            is_serialized=True,
        )
        SerialUnit.objects.create(stock_item=stock_item, serial_number="SER-001")
        CostAvailabilityProfile.objects.create(
            product=self.product,
            manufacturing_cost_usd=Decimal("6.50"),
            manufacturing_lead_time_days=5,
        )
        order = Order.objects.create(status=Order.Status.DRAFT)
        OrderItem.objects.create(order=order, product=self.product, quantity=2, unit_price_usd=self.product.price_usd)

        self.client.post(reverse("orders:order_submit", args=[order.id]), {"auto_trigger_manufacturing": "1"})

        order.refresh_from_db()
        stock_item.refresh_from_db()
        self.assertEqual(order.status, Order.Status.IN_PRODUCTION)
        self.assertEqual(stock_item.quantity, 5)
        self.assertEqual(stock_item.units.filter(status="ALLOCATED").count(), 0)
        self.assertEqual(ManufacturingOrder.objects.count(), 1)

    def test_order_quote_page_renders(self):
        order = Order.objects.create(status=Order.Status.DRAFT)
        OrderItem.objects.create(order=order, product=self.product, quantity=1, unit_price_usd=self.product.price_usd)
        response = self.client.get(reverse("orders:order_quote", args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Checkout Quote")


class APIAuthenticationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="api-user", password="StrongPass123")
        self.client = APIClient()

    def test_jwt_token_can_access_authenticated_api_route(self):
        token_response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "api-user", "password": "StrongPass123"},
            format="json",
        )
        self.assertEqual(token_response.status_code, 200)

        access_token = token_response.data["access"]
        me_response = self.client.get("/api/auth/me/", HTTP_AUTHORIZATION=f"Bearer {access_token}")

        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.data["username"], "api-user")

    def test_drf_token_can_access_authenticated_api_route(self):
        token_response = self.client.post(
            reverse("api_token_auth"),
            {"username": "api-user", "password": "StrongPass123"},
        )
        self.assertEqual(token_response.status_code, 200)

        token = token_response.data["token"]
        me_response = self.client.get("/api/auth/me/", HTTP_AUTHORIZATION=f"Token {token}")

        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.data["username"], "api-user")
