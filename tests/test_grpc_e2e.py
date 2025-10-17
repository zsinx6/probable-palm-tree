from __future__ import annotations
import asyncio
import socket
import pytest
import grpc

from app.services.orders_service import OrdersService
from app.adapters.grpc_server import start_grpc_server

from generated.orders_types_pb2 import (
    CreateOrderRequest, OrderItem, Money, GetOrderRequest, ListOrdersRequest,
)
from generated.orders_service_pb2_grpc import OrdersServiceStub

def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

@pytest.mark.asyncio
async def test_grpc_create_get_list_e2e():
    svc = OrdersService()
    port = _free_port()
    server = await start_grpc_server(svc, host="127.0.0.1", port=port)

    try:
        async with grpc.aio.insecure_channel(f"127.0.0.1:{port}") as ch:
            stub = OrdersServiceStub(ch)

            resp = await stub.CreateOrder(CreateOrderRequest(
                customer_id="C9",
                items=[OrderItem(sku="SKU-9", quantity=2, unit_price=Money(currency="BRL", units=1500, scale=2))]
            ))
            assert resp.order_id

            got = await stub.GetOrder(GetOrderRequest(order_id=resp.order_id))
            assert got.customer_id == "C9"
            assert got.total.units == 3000

            ids = []
            async for o in stub.ListOrders(ListOrdersRequest(customer_id="C9")):
                ids.append(o.order_id)
            assert resp.order_id in ids
    finally:
        await server.stop(grace=None)
