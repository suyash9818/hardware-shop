"""External Payments integration (stub) - Stripe recommended."""

import os
from dataclasses import dataclass

@dataclass
class CheckoutSession:
    id: str
    url: str

class StripePaymentGateway:
    def __init__(self):
        self.secret_key = os.getenv("STRIPE_SECRET_KEY", "")

    def is_configured(self) -> bool:
        return bool(self.secret_key)

    def create_checkout_session(self, order_id: int, amount_usd_cents: int) -> CheckoutSession:
        """Return a placeholder session.
        In production: call Stripe API to create a Checkout Session.
        """
        # NOTE: Stub for checkpoint demo.
        return CheckoutSession(id=f"cs_test_{order_id}", url=f"/orders/{order_id}/")
