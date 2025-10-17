from __future__ import annotations
import asyncio
import grpc

from generated.orders_types_pb2 import (
    CreateOrderRequest,
    OrderItem,
    Money,
    GetOrderRequest,
    ListOrdersRequest,
)
from generated.orders_service_pb2_grpc import OrdersServiceStub


async def main():
    async with grpc.aio.insecure_channel("localhost:50051") as ch:
        stub = OrdersServiceStub(ch)

        resp = await stub.CreateOrder(CreateOrderRequest(
            customer_id="c123",
            items=[
                OrderItem(
                    sku="SKU-1",
                    quantity=2,
                    unit_price=Money(currency="BRL", units=1990, scale=2),
                )
            ],
        ))
        print("created:", resp.order_id)

        order = await stub.GetOrder(GetOrderRequest(order_id=resp.order_id))
        print("order total:", order.total.units, "scale:", order.total.scale)

        async for o in stub.ListOrders(ListOrdersRequest(customer_id="c123")):
            print("stream item:", o.order_id)

if __name__ == "__main__":
    asyncio.run(main())
