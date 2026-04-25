from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from catalog.views import home

admin.site.site_header = "Hardware Shop Final Admin"
admin.site.site_title = "Hardware Shop Admin"
admin.site.index_title = "Administration"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("catalog/", include("catalog.urls")),
    path("cart/", include(("cart.urls", "cart"), namespace="cart")),
    path("orders/", include(("orders.urls", "orders"), namespace="orders")),
    path("inventory/", include(("inventory.urls", "inventory"), namespace="inventory")),
    path("pricing/", include(("pricing.urls", "pricing"), namespace="pricing")),
    path("manufacturing/", include(("manufacturing.urls", "manufacturing"), namespace="manufacturing")),
    path("rma/", include(("rma.urls", "rma"), namespace="rma")),
    path("api/", include("hardware_shop.api.urls")),

    # API auth
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/token-auth/", obtain_auth_token, name="api_token_auth"),
]
