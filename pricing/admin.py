from django.contrib import admin
from .models import Supplier, CostAvailabilityProfile, SupplierOffer, ProcurementOrder

admin.site.register(Supplier)
admin.site.register(CostAvailabilityProfile)
admin.site.register(SupplierOffer)
admin.site.register(ProcurementOrder)
