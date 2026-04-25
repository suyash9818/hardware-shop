from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, CostAvailabilityProfileViewSet, ManufacturerViewSet, ManufacturingOrderViewSet,
    OrderViewSet, ProcurementOrderViewSet, ProductViewSet, RMAViewSet, SerialUnitViewSet, StockItemViewSet,
    SupplierOfferViewSet, SupplierViewSet, api_docs, current_user,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)
router.register(r"stock", StockItemViewSet)
router.register(r"serial-units", SerialUnitViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"manufacturers", ManufacturerViewSet)
router.register(r"manufacturing-orders", ManufacturingOrderViewSet)
router.register(r"suppliers", SupplierViewSet)
router.register(r"supplier-offers", SupplierOfferViewSet)
router.register(r"cost-profiles", CostAvailabilityProfileViewSet)
router.register(r"procurement-orders", ProcurementOrderViewSet)
router.register(r"rmas", RMAViewSet)

urlpatterns = [
    path("docs/", api_docs, name="api_docs"),
    path("auth/me/", current_user, name="api_me"),
    path("", include(router.urls)),
]
