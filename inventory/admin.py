from django.contrib import admin
from .models import StockItem, SerialUnit

class SerialUnitInline(admin.TabularInline):
    model = SerialUnit
    extra = 0

@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "quantity", "is_serialized", "updated_at")
    list_filter = ("warehouse", "is_serialized")
    search_fields = ("product__sku", "product__name")
    inlines = [SerialUnitInline]

@admin.register(SerialUnit)
class SerialUnitAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "stock_item", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("serial_number", "stock_item__product__sku", "stock_item__product__name")
