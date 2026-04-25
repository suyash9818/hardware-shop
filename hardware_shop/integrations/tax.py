"""External Tax calculation integration (stub) - TaxJar or Avalara recommended."""

import os

class TaxGateway:
    def __init__(self):
        self.taxjar_token = os.getenv("TAXJAR_API_TOKEN", "")

    def is_configured(self) -> bool:
        return bool(self.taxjar_token)

    def estimate_tax(self, amount_usd: float, state: str) -> float:
        """Mock tax estimate for demo."""
        # Example: flat 8.25% for CA in demo mode (do not use for production).
        if state.upper() == "CA":
            return round(amount_usd * 0.0825, 2)
        return round(amount_usd * 0.05, 2)
