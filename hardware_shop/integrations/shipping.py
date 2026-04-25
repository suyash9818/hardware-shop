"""External Shipping integration (stub) - Shippo or EasyPost recommended."""

import os
from dataclasses import dataclass

@dataclass
class ShippingRate:
    carrier: str
    service: str
    amount_usd: float
    eta_days: int

class ShippingGateway:
    def __init__(self):
        self.shippo_token = os.getenv("SHIPPO_API_TOKEN", "")
        self.easypost_key = os.getenv("EASYPOST_API_KEY", "")

    def is_configured(self) -> bool:
        return bool(self.shippo_token or self.easypost_key)

    def get_rates(self, to_zip: str, weight_oz: float):
        """Return mock rates for demo."""
        return [
            ShippingRate(carrier="USPS", service="Ground Advantage", amount_usd=6.95, eta_days=4),
            ShippingRate(carrier="UPS", service="UPS Ground", amount_usd=12.50, eta_days=3),
        ]
