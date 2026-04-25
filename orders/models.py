
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import DecimalField, ExpressionWrapper, F, Sum


class Order(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        RESERVED = "RESERVED", "Inventory Reserved"
        IN_PRODUCTION = "IN_PRODUCTION", "In Production"
        FULFILLED = "FULFILLED", "Fulfilled"
        READY = "READY", "Ready"
        CANCELLED = "CANCELLED", "Cancelled"

    class PaymentStatus(models.TextChoices):
        UNPAID = "UNPAID", "Unpaid"
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_session_id = models.CharField(max_length=120, blank=True, default="")
    payment_reference = models.CharField(max_length=120, blank=True, default="")
    payment_method_label = models.CharField(max_length=80, blank=True, default="")
    paid_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} ({self.status})"

    @property
    def total_usd(self):
        line_total = ExpressionWrapper(
            F("quantity") * F("unit_price_usd"),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )
        total = self.items.aggregate(total=Sum(line_total))["total"]
        return total or Decimal("0.00")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("catalog.Product", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.order} - {self.product.sku} x{self.quantity}"

    @property
    def line_total(self):
        return self.quantity * self.unit_price_usd
