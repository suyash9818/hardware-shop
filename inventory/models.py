from django.db import models

from catalog.models import Product


class StockItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="stock_item")
    warehouse = models.CharField(max_length=120, default="Main Warehouse")
    quantity = models.PositiveIntegerField(default=0)
    is_serialized = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.warehouse}"


class SerialUnit(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        ALLOCATED = "ALLOCATED", "Allocated"
        SOLD = "SOLD", "Sold"
        RETURNED = "RETURNED", "Returned"

    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name="units")
    serial_number = models.CharField(max_length=80, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.serial_number
