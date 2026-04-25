from django.test import TestCase
from django.urls import reverse
from decimal import Decimal

from catalog.models import Category, Product
from orders.models import Order
from .models import RMA


class RMATests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Returns", slug="returns")
        self.product = Product.objects.create(sku="RET-001", name="Warranty Tool", category=category, price_usd=Decimal("10.00"), specs={})
        self.order = Order.objects.create()

    def test_create_rma(self):
        response = self.client.post(reverse("rma:rma_create"), {
            "order": self.order.id,
            "product": self.product.id,
            "customer_email": "test@example.com",
            "reason": "Defective on arrival",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RMA.objects.count(), 1)
