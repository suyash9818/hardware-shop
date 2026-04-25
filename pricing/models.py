from django.db import models
from catalog.models import Product

class Supplier(models.Model):
    name = models.CharField(max_length=200, unique=True)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class SupplierOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="supplier_offers")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name="offers")

    purchase_cost_usd = models.DecimalField(max_digits=10, decimal_places=2)
    lead_time_days = models.PositiveIntegerField(default=7)
    min_order_qty = models.PositiveIntegerField(default=1)
    available_qty = models.PositiveIntegerField(default=0, help_text="Supplier-reported availability (optional).")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("product", "supplier")]
        ordering = ["product__sku", "purchase_cost_usd"]

    def __str__(self) -> str:
        return f"{self.supplier.name} -> {self.product.sku}"


class CostAvailabilityProfile(models.Model):
    """Optional per-product profile for cost/availability decisions (v2)."""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="cost_profile")
    manufacturing_cost_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    manufacturing_lead_time_days = models.PositiveIntegerField(default=14)
    reorder_point = models.PositiveIntegerField(default=0, help_text="If on-hand qty drops below this, consider manufacturing/procurement.")
    reorder_qty = models.PositiveIntegerField(default=0, help_text="Suggested replenishment qty for auto-triggering.")

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"CostProfile({self.product.sku})"


class ProcurementOrder(models.Model):
    STATUS_CHOICES = [
        ("PLANNED", "Planned"),
        ("ORDERED", "Ordered"),
        ("RECEIVED", "Received"),
        ("CANCELLED", "Cancelled"),
    ]

    order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL, null=True, blank=True, related_name="procurements")
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_cost_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PLANNED")
    expected_delivery = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PO-{self.id} {self.product.sku} x{self.quantity} ({self.status})"
