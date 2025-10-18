from __future__ import annotations
import grpc
from typing import AsyncIterator

from generated.orders_types_pb2 import (
    Order as PbOrder,
    CreateOrderRequest as PbCreateOrderRequest,
    CreateOrderResponse as PbCreateOrderResponse,
    GetOrderRequest as PbGetOrderRequest,
    ListOrdersRequest as PbListOrdersRequest,
)

from app.domain.orders import OrderItem
from generated.orders_service_pb2_grpc import (
    OrdersServiceServicer,
    add_OrdersServiceServicer_to_server,
)

from app.services.orders_service import OrdersService


class OrdersGrpc(OrdersServiceServicer):
    def __init__(self, svc: OrdersService) -> None:
        self.svc = svc

    async def CreateOrder(
        self, request: PbCreateOrderRequest, context
    ) -> PbCreateOrderResponse:
        items = [OrderItem.from_proto(i) for i in request.items]
        order_id = await self.svc.create_order(request.customer_id, items)
        return PbCreateOrderResponse(order_id=order_id)

    async def GetOrder(self, request: PbGetOrderRequest, context) -> PbOrder:
        o = await self.svc.get_order(request.order_id)
        return o.to_proto()

    async def ListOrders(
        self, request: PbListOrdersRequest, context
    ) -> AsyncIterator[PbOrder]:
        async for o in self.svc.stream_orders_by_customer(request.customer_id):
            yield o.to_proto()


async def start_grpc_server(
    svc: OrdersService, host: str = "0.0.0.0", port: int = 50051
):
    server = grpc.aio.server()
    add_OrdersServiceServicer_to_server(OrdersGrpc(svc), server)
    server.add_insecure_port(f"{host}:{port}")
    await server.start()
    return server
