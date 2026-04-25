from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class CatalogViewsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Connectors", slug="connectors")

    def test_search_returns_matching_product_by_specs(self):
        matching = Product.objects.create(
            sku="M12-CONN",
            name="M12 Connector",
            category=self.category,
            price_usd=Decimal("9.99"),
            specs={"thread": "M12", "voltage": "24V"},
        )
        Product.objects.create(
            sku="M8-CONN",
            name="M8 Connector",
            category=self.category,
            price_usd=Decimal("8.99"),
            specs={"thread": "M8", "voltage": "12V"},
        )

        response = self.client.get(reverse("search"), {"q": "M12"})

        self.assertEqual(response.status_code, 200)
        products = list(response.context["products"])
        self.assertIn(matching, products)
        self.assertEqual(products, [matching])

    def test_product_detail_context_includes_compatible_products(self):
        source = Product.objects.create(
            sku="SRC-001",
            name="Source Product",
            category=self.category,
            price_usd=Decimal("19.99"),
            specs={"thread": "M12", "voltage": "24V"},
        )
        compatible = Product.objects.create(
            sku="CMP-001",
            name="Compatible Product",
            category=self.category,
            price_usd=Decimal("21.99"),
            specs={"thread": "M12", "voltage": "48V"},
        )
        Product.objects.create(
            sku="OTHER-001",
            name="Other Product",
            category=self.category,
            price_usd=Decimal("5.00"),
            specs={"thread": "M8", "voltage": "12V"},
        )

        response = self.client.get(reverse("product_detail", args=[source.id]))

        self.assertEqual(response.status_code, 200)
        compatible_products = list(response.context["compatible_products"])
        self.assertIn(compatible, compatible_products)
        self.assertEqual(len(compatible_products), 1)
