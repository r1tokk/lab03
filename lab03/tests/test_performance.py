from typing import Any

from model import Item, Order, make_meta


def test_subtotal_benchmark(benchmark: Any) -> None:
    """Вимірює час виконання обчислення суми (subtotal) для великого замовлення."""
    items = tuple(Item(f"SKU{i}", 10.0, 2) for i in range(1000))
    tags = frozenset({"test", "bulk"})
    meta = make_meta(source="benchmark")
    order = Order(id=1, paid=True, items=items, tags=tags, meta=meta)

    benchmark(lambda: order.subtotal())
