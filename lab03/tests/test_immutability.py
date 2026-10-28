import pytest

from core import add_item_to_order, add_vip_tag
from model import Item, Order, make_meta


@pytest.fixture
def sample_order() -> Order:
    items = (Item("A1", 50.0, 2), Item("B2", 20.0, 1))
    tags = frozenset({"delhi", "priority"})
    meta = make_meta(source="fb_ads", campaign="summer")
    return Order(id=10, paid=False, items=items, tags=tags, meta=meta)


def test_no_mutation_when_adding_item(sample_order: Order) -> None:
    """Перевірка референтної прозорості та відсутності мутацій."""
    original_items_len = len(sample_order.items)

    new_order = add_item_to_order(sample_order, "C3", 15.0, 2)

    assert len(sample_order.items) == original_items_len
    assert new_order is not sample_order
    assert new_order.subtotal() == sample_order.subtotal() + 30.0


def test_hashability(sample_order: Order) -> None:
    """Перевірка використання Order як ключа завдяки frozen-властивостям."""
    new_order = add_item_to_order(sample_order, "C3", 15.0, 2)
    orders_set = {sample_order, new_order}
    assert len(orders_set) == 2


def test_mappingproxy_is_read_only(sample_order: Order) -> None:
    """Перевірка того, що MappingProxyType кидає TypeError при зміні."""
    with pytest.raises(TypeError):
        sample_order.meta["source"] = "changed"  # type: ignore[index]


def test_add_vip_tag(sample_order: Order) -> None:
    new_order = add_vip_tag(sample_order)
    assert "vip" in new_order.tags
    assert "vip" not in sample_order.tags
