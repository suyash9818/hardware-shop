from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from .models import Order
from .decision import decide_fulfillment, apply_fulfillment

def submit_order(order: Order, auto_trigger_manufacturing: bool = True) -> dict:
    """
    Submit an order and automatically decide fulfillment.

    Lifecycle:
      DRAFT -> SUBMITTED -> (FULFILLED or IN_PRODUCTION)
    """
    if order.status != Order.Status.DRAFT:
        return {"ok": False, "message": f"Order must be DRAFT to submit (current={order.status})."}

    with transaction.atomic():
        order.status = Order.Status.SUBMITTED
        order.submitted_at = timezone.now()
        order.save()

        decision = decide_fulfillment(order)

        # Apply decision: decrement/reserve inventory, or create procurement/manufacturing records
        apply_fulfillment(order, decision, auto_create_records=auto_trigger_manufacturing)

        if decision["source"] == "INVENTORY":
            order.status = Order.Status.FULFILLED
        else:
            # supplier/manufacturing work is pending
            order.status = Order.Status.IN_PRODUCTION

        order.notes = (order.notes or "") + f"\nDecision: {decision}"
        order.save()

    return {"ok": True, "decision": decision, "order_id": order.id, "new_status": order.status}
