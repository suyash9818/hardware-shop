from rest_framework import serializers
from catalog.models import Category, Product
from inventory.models import StockItem, SerialUnit
from orders.models import Order, OrderItem
from manufacturing.models import Manufacturer, ManufacturingOrder
from pricing.models import Supplier, SupplierOffer, CostAvailabilityProfile, ProcurementOrder

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(source="category", queryset=Category.objects.all(), write_only=True)

    class Meta:
        model = Product
        fields = ["id", "sku", "name", "category", "category_id", "description", "price_usd", "specs", "created_at"]

class StockItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(source="product", queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = StockItem
        fields = ["id", "product", "product_id", "warehouse", "quantity", "is_serialized", "updated_at"]

class SerialUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerialUnit
        fields = ["id", "stock_item", "serial_number", "status", "created_at"]

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(source="product", queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_id", "quantity", "unit_price_usd", "line_total"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_usd = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "status", "notes", "created_at", "submitted_at", "items", "total_usd"]

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ["id", "name", "location", "capabilities", "contact_email"]

class ManufacturingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturingOrder
        fields = ["id", "product", "manufacturer", "quantity", "unit_cost_usd", "status", "expected_delivery", "created_at", "updated_at"]

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "website", "contact_email"]

class SupplierOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierOffer
        fields = ["id", "product", "supplier", "purchase_cost_usd", "lead_time_days", "min_order_qty", "available_qty", "updated_at"]

class CostAvailabilityProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostAvailabilityProfile
        fields = ["id", "product", "manufacturing_cost_usd", "manufacturing_lead_time_days", "reorder_point", "reorder_qty", "updated_at"]


class ProcurementOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcurementOrder
        fields = ["id", "order", "product", "supplier", "quantity", "unit_cost_usd", "status", "expected_delivery", "created_at"]


from rma.models import RMA

class RMASerializer(serializers.ModelSerializer):
    class Meta:
        model = RMA
        fields = ["id", "order", "product", "serial_unit", "customer_email", "reason", "status", "resolution_notes", "created_at", "updated_at"]
