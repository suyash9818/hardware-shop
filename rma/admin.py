from django.contrib import admin

from .models import RMA


@admin.register(RMA)
class RMAAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "order", "status", "customer_email", "created_at")
    list_filter = ("status",)
    search_fields = ("product__sku", "product__name", "customer_email")
