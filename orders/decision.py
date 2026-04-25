from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List, Optional

from django.utils import timezone
import datetime

from inventory.models import StockItem
from pricing.models import SupplierOffer, CostAvailabilityProfile
from manufacturing.models import Manufacturer, ManufacturingOrder
from .models import Order

@dataclass
class FulfillmentChoice:
    source: str  # INVENTORY | SUPPLIER | MANUFACTURING
    cost_usd: Decimal
    eta_days: int
    explanation: str
    supplier_offer_id: Optional[int] = None

def _inventory_choice(product_id: int, needed_qty: int) -> Optional[FulfillmentChoice]:
    stock = StockItem.objects.filter(product_id=product_id).first()
    if not stock:
        return None
    available_qty = int(stock.quantity)
    if stock.is_serialized:
        available_qty = stock.units.filter(status="AVAILABLE").count()
    if available_qty >= needed_qty:
        return FulfillmentChoice(
            source="INVENTORY",
            cost_usd=Decimal("0.00"),
            eta_days=0,
            explanation=f"Enough on-hand inventory (qty={available_qty}) to fulfill required qty={needed_qty}.",
        )
    return None

def _best_supplier_choice(product_id: int, needed_qty: int) -> Optional[FulfillmentChoice]:
    offers = SupplierOffer.objects.filter(product_id=product_id).order_by("purchase_cost_usd", "lead_time_days")
    best = None
    for o in offers:
        if o.available_qty < needed_qty:
            continue
        if needed_qty < o.min_order_qty:
            continue
        cost = (o.purchase_cost_usd * Decimal(needed_qty))
        choice = FulfillmentChoice(
            source="SUPPLIER",
            cost_usd=cost,
            eta_days=int(o.lead_time_days),
            explanation=f"Supplier {o.supplier.name}: cost ${o.purchase_cost_usd}/unit, lead time {o.lead_time_days} days.",
            supplier_offer_id=o.id,
        )
        best = choice
        break
    return best

def _manufacturing_choice(product_id: int, needed_qty: int) -> Optional[FulfillmentChoice]:
    profile = CostAvailabilityProfile.objects.filter(product_id=product_id).first()
    if not profile:
        return None
    cost = (profile.manufacturing_cost_usd * Decimal(needed_qty))
    return FulfillmentChoice(
        source="MANUFACTURING",
        cost_usd=cost,
        eta_days=int(profile.manufacturing_lead_time_days),
        explanation=f"In-house/contract manufacturing: cost ${profile.manufacturing_cost_usd}/unit, lead time {profile.manufacturing_lead_time_days} days.",
    )

def decide_fulfillment(order: Order) -> Dict:
    """
    Decide how to fulfill an order.
    Returns:
      {
        "source": "INVENTORY"|"MIXED"|"SUPPLIER"|"MANUFACTURING",
        "cost_usd": "123.45",
        "eta_days": 7,
        "explanation": "...",
        "items": [{"product_id":..,"qty":..,"choice":{...}}, ...]
      }
    """
    items = order.items.select_related("product").all()
    item_decisions: List[Dict] = []
    total_cost = Decimal("0.00")
    eta_days = 0
    sources = set()

    for it in items:
        pid = it.product_id
        qty = int(it.quantity)

        inv = _inventory_choice(pid, qty)
        if inv:
            choice = inv
        else:
            sup = _best_supplier_choice(pid, qty)
            mfg = _manufacturing_choice(pid, qty)

            # pick best based on cost then eta; if one missing, choose the other
            candidates = [c for c in [sup, mfg] if c is not None]
            if not candidates:
                # no data - default to manufacturing order with unknown cost
                choice = FulfillmentChoice(
                    source="MANUFACTURING",
                    cost_usd=Decimal("0.00"),
                    eta_days=14,
                    explanation="No supplier offers or cost profile found; defaulting to manufacturing (placeholder).",
                )
            else:
                candidates.sort(key=lambda c: (c.cost_usd, c.eta_days))
                choice = candidates[0]

        sources.add(choice.source)
        total_cost += choice.cost_usd
        eta_days = max(eta_days, choice.eta_days)

        item_decisions.append({
            "product_id": pid,
            "sku": it.product.sku,
            "name": it.product.name,
            "qty": qty,
            "choice": {
                "source": choice.source,
                "cost_usd": str(choice.cost_usd),
                "eta_days": choice.eta_days,
                "explanation": choice.explanation,
                "supplier_offer_id": choice.supplier_offer_id,
            }
        })

    overall_source = list(sources)[0] if len(sources) == 1 else "MIXED"
    explanation = " | ".join([f"{d['sku']}: {d['choice']['source']}" for d in item_decisions])

    return {
        "source": overall_source,
        "cost_usd": str(total_cost),
        "eta_days": int(eta_days),
        "explanation": explanation,
        "items": item_decisions,
    }

def apply_fulfillment(order: Order, decision: Dict, auto_create_records: bool = True) -> None:
    """
    Apply a decision to the system:
    - If INVENTORY: decrement stock (and allocate serials if serialized)
    - If SUPPLIER: create ProcurementOrder (if enabled)
    - If MANUFACTURING: create ManufacturingOrder(s)
    """
    from pricing.models import ProcurementOrder  # imported here to avoid circular imports
    for d in decision["items"]:
        pid = d["product_id"]
        qty = int(d["qty"])
        src = d["choice"]["source"]

        if src == "INVENTORY":
            stock = StockItem.objects.select_for_update().filter(product_id=pid).first()
            if stock:
                stock.quantity = max(0, stock.quantity - qty)
                stock.save()
                if stock.is_serialized:
                    units = stock.units.filter(status="AVAILABLE")[:qty]
                    for u in units:
                        u.status = "ALLOCATED"
                        u.save()

        elif src == "SUPPLIER" and auto_create_records:
            offer_id = d["choice"].get("supplier_offer_id")
            offer = SupplierOffer.objects.filter(id=offer_id).select_related("supplier").first() if offer_id else None
            supplier = offer.supplier if offer else None
            unit_cost = offer.purchase_cost_usd if offer else Decimal("0.00")
            eta = int(offer.lead_time_days) if offer else 7
            expected = timezone.now().date() + datetime.timedelta(days=eta)

            if supplier:
                ProcurementOrder.objects.create(
                    product_id=pid,
                    supplier=supplier,
                    quantity=qty,
                    unit_cost_usd=unit_cost,
                    status="PLANNED",
                    expected_delivery=expected,
                    order=order,
                )

        elif src == "MANUFACTURING" and auto_create_records:
            profile = CostAvailabilityProfile.objects.filter(product_id=pid).first()
            unit_cost = profile.manufacturing_cost_usd if profile else Decimal("0.00")
            eta = int(profile.manufacturing_lead_time_days) if profile else 14
            expected = timezone.now().date() + datetime.timedelta(days=eta)
            mfg = Manufacturer.objects.first() or Manufacturer.objects.create(name="Default Manufacturer")
            ManufacturingOrder.objects.create(
                product_id=pid,
                manufacturer=mfg,
                quantity=qty,
                unit_cost_usd=unit_cost,
                status="PLANNED",
                expected_delivery=expected,
            )
