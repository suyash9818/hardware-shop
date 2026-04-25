from django.contrib import admin
from .models import Manufacturer, ManufacturingOrder

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "contact_email")
    search_fields = ("name", "location", "contact_email")

@admin.register(ManufacturingOrder)
class ManufacturingOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "manufacturer", "quantity", "status", "expected_delivery", "created_at")
    list_filter = ("status", "manufacturer")
    search_fields = ("product__sku", "product__name", "manufacturer__name")
