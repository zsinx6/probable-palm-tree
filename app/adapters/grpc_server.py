from __future__ import annotations
import grpc
from typing import AsyncIterator

from generated.orders_types_pb2 import (
    Money as PbMoney,
    Order as PbOrder,
    OrderItem as PbOrderItem,
    CreateOrderRequest as PbCreateOrderRequest,
    CreateOrderResponse as PbCreateOrderResponse,
    GetOrderRequest as PbGetOrderRequest,
    ListOrdersRequest as PbListOrdersRequest,
    HealthCheckRequest as PbHealthCheckRequest,
    HealthCheckResponse as PbHealthCheckResponse,
)
from generated.orders_service_pb2_grpc import (
    OrdersServiceServicer,
    add_OrdersServiceServicer_to_server,
)

from app.services.orders_service import OrdersService
from app.domain.orders import OrderItem, Money


def money_to_pb(m: Money) -> PbMoney:
    return PbMoney(currency=m.currency, units=m.units, scale=m.scale)


class OrdersGrpc(OrdersServiceServicer):
    def __init__(self, svc: OrdersService) -> None:
        self.svc = svc

    async def CreateOrder(self, request: PbCreateOrderRequest, context) -> PbCreateOrderResponse:
        items = [
            OrderItem(
                sku=i.sku,
                quantity=i.quantity,
                unit_price=Money(currency=i.unit_price.currency, units=i.unit_price.units, scale=i.unit_price.scale),
            )
            for i in request.items
        ]
        order_id = await self.svc.create_order(request.customer_id, items)
        return PbCreateOrderResponse(order_id=order_id)

    async def GetOrder(self, request: PbGetOrderRequest, context) -> PbOrder:
        o = await self.svc.get_order(request.order_id)
        return PbOrder(
            order_id=o.order_id,
            customer_id=o.customer_id,
            items=[PbOrderItem(sku=i.sku, quantity=i.quantity, unit_price=money_to_pb(i.unit_price)) for i in o.items],
            total=money_to_pb(o.total),
            status=o.status,
        )

    async def ListOrders(self, request: PbListOrdersRequest, context) -> AsyncIterator[PbOrder]:
        async for o in self.svc.stream_orders_by_customer(request.customer_id):
            yield PbOrder(
                order_id=o.order_id,
                customer_id=o.customer_id,
                items=[PbOrderItem(sku=i.sku, quantity=i.quantity, unit_price=money_to_pb(i.unit_price)) for i in o.items],
                total=money_to_pb(o.total),
                status=o.status,
            )

    async def HealthCheck(self, request: PbHealthCheckRequest, context) -> PbHealthCheckResponse:
        return PbHealthCheckResponse(status="SERVING")


async def start_grpc_server(svc: OrdersService, host: str = "0.0.0.0", port: int = 50051):
    server = grpc.aio.server()
    add_OrdersServiceServicer_to_server(OrdersGrpc(svc), server)
    server.add_insecure_port(f"{host}:{port}")
    await server.start()
    return server
