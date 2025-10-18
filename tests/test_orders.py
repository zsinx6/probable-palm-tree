from __future__ import annotations

import pytest
from app.services.orders_service import OrdersService
from app.domain.orders import OrderItem, Money


@pytest.mark.asyncio
async def test_create_and_get():
    svc = OrdersService()
    order_id = await svc.create_order(
        "c1",
        [
            OrderItem(
                sku="A",
                quantity=1,
                unit_price=Money(currency="BRL", units=100, scale=2),
            )
        ],
    )
    got = await svc.get_order(order_id)
    assert got.order_id == order_id
    assert got.total.units == 100
