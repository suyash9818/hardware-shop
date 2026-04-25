from django.db import models
from catalog.models import Product

class Manufacturer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=200, blank=True)
    capabilities = models.TextField(blank=True, help_text="Notes about what this manufacturer can produce.")
    contact_email = models.EmailField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class ManufacturingOrder(models.Model):
    STATUS_CHOICES = [
        ("PLANNED", "Planned"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="mfg_orders")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, related_name="orders")
    quantity = models.PositiveIntegerField()
    unit_cost_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PLANNED")
    expected_delivery = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"MO#{self.id} {self.product.sku} x{self.quantity} ({self.status})"
