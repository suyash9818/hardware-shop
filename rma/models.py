from django.db import models


class RMA(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "REQUESTED", "Requested"
        APPROVED = "APPROVED", "Approved"
        IN_TRANSIT = "IN_TRANSIT", "In Transit"
        RECEIVED = "RECEIVED", "Received"
        RESOLVED = "RESOLVED", "Resolved"
        REJECTED = "REJECTED", "Rejected"

    order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL, null=True, blank=True, related_name="rmas")
    product = models.ForeignKey("catalog.Product", on_delete=models.PROTECT, related_name="rmas")
    serial_unit = models.ForeignKey("inventory.SerialUnit", on_delete=models.SET_NULL, null=True, blank=True, related_name="rmas")
    customer_email = models.EmailField(blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"RMA-{self.id} {self.product.sku} ({self.status})"
