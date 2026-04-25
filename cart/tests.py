from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product
from .models import CartItem


class CartViewsTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Tools", slug="tools")
        self.product = Product.objects.create(
            sku="TOOL-001",
            name="Crimping Tool",
            category=category,
            price_usd=Decimal("49.99"),
            specs={},
        )

    def test_add_to_cart_creates_item_and_second_add_increments_quantity(self):
        add_url = reverse("cart:add_to_cart", args=[self.product.id])

        first = self.client.get(add_url)
        second = self.client.get(add_url)

        self.assertEqual(first.status_code, 302)
        self.assertEqual(second.status_code, 302)

        item = CartItem.objects.get(product=self.product)
        self.assertEqual(item.quantity, 2)

        cart_page = self.client.get(reverse("cart:view_cart"))
        self.assertEqual(cart_page.status_code, 200)
        self.assertContains(cart_page, "Crimping Tool")
