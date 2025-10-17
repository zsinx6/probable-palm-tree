from __future__ import annotations
from typing import List, Self
from pydantic import Field

from app.domain.base import ProtoModel

from generated.orders_types_pb2 import (
    Money as PbMoney,
    OrderItem as PbOrderItem,
    Order as PbOrder,
)

class Money(ProtoModel[PbMoney]):
    currency: str = Field(description="Código da moeda (ex.: 'BRL').")
    units: int = Field(description="Valor inteiro na escala definida.")
    scale: int = Field(default=2, description="Casas decimais (escala).")

    def to_proto(self) -> PbMoney:
        return PbMoney(currency=self.currency, units=self.units, scale=self.scale)

    @classmethod
    def from_proto(cls, pb: PbMoney) -> Self:
        return cls(currency=pb.currency, units=pb.units, scale=pb.scale)


class OrderItem(ProtoModel[PbOrderItem]):
    sku: str
    quantity: int
    unit_price: Money

    def to_proto(self) -> PbOrderItem:
        return PbOrderItem(
            sku=self.sku,
            quantity=self.quantity,
            unit_price=self.unit_price.to_proto(),
        )

    @classmethod
    def from_proto(cls, pb: PbOrderItem) -> Self:
        return cls(
            sku=pb.sku,
            quantity=pb.quantity,
            unit_price=Money.from_proto(pb.unit_price),
        )


class Order(ProtoModel[PbOrder]):
    order_id: str
    customer_id: str
    items: List[OrderItem]
    total: Money
    status: str = "CREATED"

    def to_proto(self) -> PbOrder:
        return PbOrder(
            order_id=self.order_id,
            customer_id=self.customer_id,
            items=[i.to_proto() for i in self.items],
            total=self.total.to_proto(),
            status=self.status,
        )

    @classmethod
    def from_proto(cls, pb: PbOrder) -> Self:
        return cls(
            order_id=pb.order_id,
            customer_id=pb.customer_id,
            items=[OrderItem.from_proto(i) for i in pb.items],
            total=Money.from_proto(pb.total),
            status=pb.status,
        )
