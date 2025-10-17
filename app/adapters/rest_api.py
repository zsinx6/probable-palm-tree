from __future__ import annotations

from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List

from app.services.orders_service import OrdersService
from app.domain.orders import OrderItem, Money


app = FastAPI()

class MoneyIn(BaseModel):
    currency: str = "BRL"
    units: int
    scale: int = 2

class OrderItemIn(BaseModel):
    sku: str
    quantity: int
    unit_price: MoneyIn

class CreateOrderIn(BaseModel):
    customer_id: str
    items: List[OrderItemIn]

def mount_routes(app: FastAPI, svc: OrdersService) -> None:
    @app.get("/health")
    async def healthz():
        return {"status": "ok"}

    @app.post("/orders")
    async def create_order(body: CreateOrderIn):
        items = [
            OrderItem(
                sku=i.sku,
                quantity=i.quantity,
                unit_price=Money(**i.unit_price.model_dump()),
            )
            for i in body.items
        ]
        order_id = await svc.create_order(body.customer_id, items)
        return {"order_id": order_id}

    @app.get("/orders")
    async def list_orders(customer_id: str = Query(..., description="Filtra por cliente")):
        out: List[dict] = []
        async for o in svc.stream_orders_by_customer(customer_id):
            out.append(o.model_dump())
        return out
