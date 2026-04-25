import os
import secrets
from datetime import date
from dataclasses import dataclass


@dataclass
class CheckoutSession:
    id: str
    url: str
    provider: str


@dataclass
class PaymentResult:
    ok: bool
    reference: str = ""
    message: str = ""
    method_label: str = ""


class StripePaymentGateway:
    def __init__(self):
        self.secret_key = os.getenv("STRIPE_SECRET_KEY", "")

    def is_configured(self) -> bool:
        return bool(self.secret_key)

    def create_checkout_session(self, order_id: int, amount_usd_cents: int) -> CheckoutSession:
        """Return a local checkout session.

        When STRIPE_SECRET_KEY is configured this class is ready to be replaced
        with the Stripe SDK call. In demo mode, the session points to the local
        hosted payment page and never stores card data.
        """
        session_id = f"cs_demo_{order_id}_{secrets.token_hex(4)}"
        return CheckoutSession(id=session_id, url=f"/orders/{order_id}/pay/?session={session_id}", provider="stripe-demo")

    def process_demo_card(
        self,
        *,
        amount_usd_cents: int,
        card_number: str,
        exp_month: str,
        exp_year: str,
        cvc: str,
        name: str,
    ) -> PaymentResult:
        digits = "".join(ch for ch in card_number if ch.isdigit())
        cvc_digits = "".join(ch for ch in cvc if ch.isdigit())

        if amount_usd_cents <= 0:
            return PaymentResult(False, message="Payment amount must be greater than zero.")
        if len(digits) < 12 or len(digits) > 19:
            return PaymentResult(False, message="Enter a valid demo card number.")
        if len(cvc_digits) not in {3, 4}:
            return PaymentResult(False, message="Enter a valid CVC.")
        if not name.strip():
            return PaymentResult(False, message="Enter the cardholder name.")

        try:
            month = int(exp_month)
            year = int(exp_year)
        except ValueError:
            return PaymentResult(False, message="Enter a valid expiration date.")

        if year < 100:
            year += 2000
        today = date.today()
        if month < 1 or month > 12 or (year, month) < (today.year, today.month):
            return PaymentResult(False, message="The card expiration date is not valid.")

        brand = self._detect_brand(digits)
        return PaymentResult(
            True,
            reference=f"pay_demo_{secrets.token_hex(8)}",
            message="Demo payment approved.",
            method_label=f"{brand} ending {digits[-4:]}",
        )

    @staticmethod
    def _detect_brand(card_number: str) -> str:
        if card_number.startswith("4"):
            return "Visa"
        if card_number[:2] in {"51", "52", "53", "54", "55"}:
            return "Mastercard"
        if card_number.startswith(("34", "37")):
            return "Amex"
        return "Card"
