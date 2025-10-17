from __future__ import annotations
import pytest
from app.services.orders_service import OrdersService
from app.domain.orders import OrderItem, Money

@pytest.mark.asyncio
async def test_stream_orders_by_customer_filters_correctly():
    svc = OrdersService()

    for cid in ["C1", "C2", "C1"]:
        await svc.create_order(
            customer_id=cid,
            items=[OrderItem(sku="X", quantity=1, unit_price=Money(currency="BRL", units=100, scale=2))]
        )

    got_ids = []
    async for o in svc.stream_orders_by_customer("C1"):
        got_ids.append(o.customer_id)

    assert got_ids and all(cid == "C1" for cid in got_ids)
