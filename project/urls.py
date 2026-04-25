"""Legacy compatibility URLConf.

The active project setting uses `hardware_shop.urls`.
Keeping this file as a shim avoids confusion if older tooling imports it.
"""

from hardware_shop.urls import urlpatterns
