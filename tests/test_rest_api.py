from __future__ import annotations
import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from app.adapters.rest_api import mount_routes
from app.services.orders_service import OrdersService

@pytest.mark.asyncio
async def test_rest_create_order_and_health():
    svc = OrdersService()
    app = FastAPI()
    mount_routes(app, svc)

    transport = ASGITransport(app=app)
    try:
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            r = await ac.get("/health")
            assert r.status_code == 200
            assert r.json()["status"] == "ok"

            payload = {
                "customer_id": "C3",
                "items": [{"sku": "ABC", "quantity": 1,
                           "unit_price": {"currency": "BRL", "units": 2500, "scale": 2}}],
            }
            r = await ac.post("/orders", json=payload)
            assert r.status_code == 200
            order_id = r.json()["order_id"]
            assert isinstance(order_id, str) and order_id
    finally:
        await transport.aclose()
