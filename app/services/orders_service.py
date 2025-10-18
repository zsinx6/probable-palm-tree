from __future__ import annotations
import uuid
from typing import AsyncIterator

from app.domain.orders import Order, OrderItem, Money


class OrdersService:
    def __init__(self) -> None:
        self._store: dict[str, Order] = {}

    async def create_order(self, customer_id: str, items: list[OrderItem]) -> str:
        total_units = sum(i.quantity * i.unit_price.units for i in items)
        scale = items[0].unit_price.scale if items else 2
        currency = items[0].unit_price.currency if items else "BRL"

        order = Order(
            order_id=str(uuid.uuid4()),
            customer_id=customer_id,
            items=items,
            total=Money(currency=currency, units=total_units, scale=scale),
        )
        self._store[order.order_id] = order
        return order.order_id

    async def get_order(self, order_id: str) -> Order:
        return self._store[order_id]

    async def stream_orders_by_customer(self, customer_id: str) -> AsyncIterator[Order]:
        for o in self._store.values():
            if o.customer_id == customer_id:
                yield o
