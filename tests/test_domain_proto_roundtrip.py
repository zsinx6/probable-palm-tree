from __future__ import annotations
from generated.orders_types_pb2 import Money as PbMoney, OrderItem as PbOrderItem, Order as PbOrder
from app.domain.orders import Money, OrderItem, Order

def test_money_roundtrip_proto():
    m = Money(currency="BRL", units=1234, scale=2)
    pb = m.to_proto()
    assert isinstance(pb, PbMoney)
    m2 = Money.from_proto(pb)
    assert m2 == m

def test_orderitem_roundtrip_proto():
    oi = OrderItem(sku="SKU-1", quantity=3, unit_price=Money(currency="BRL", units=990, scale=2))
    pb = oi.to_proto()
    assert isinstance(pb, PbOrderItem)
    oi2 = OrderItem.from_proto(pb)
    assert oi2 == oi

def test_order_roundtrip_proto():
    o = Order(
        order_id="OID-1",
        customer_id="C1",
        items=[OrderItem(sku="A", quantity=1, unit_price=Money(currency="BRL", units=100, scale=2))],
        total=Money(currency="BRL", units=100, scale=2),
        status="CREATED",
    )
    pb = o.to_proto()
    assert isinstance(pb, PbOrder)
    o2 = Order.from_proto(pb)
    assert o2 == o
