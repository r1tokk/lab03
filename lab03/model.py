from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from types import MappingProxyType


@dataclass(frozen=True, slots=True)
class Item:
    sku: str
    price: float
    qty: int


def make_meta(**kwargs: str) -> MappingProxyType[str, str]:
    """Створює тільки-читання view над dict."""
    base = dict(kwargs)
    return MappingProxyType(base)


@dataclass(frozen=True, slots=True)
class Order:
    id: int
    paid: bool
    items: tuple[Item, ...]
    tags: frozenset[str]
    meta: Mapping[str, str] = field(hash=False)

    def subtotal(self) -> float:
        """Обчислює загальну суму замовлення."""
        return sum(i.price * i.qty for i in self.items)

    def add_tag(self, tag: str) -> Order:
        """Додає тег, повертаючи нову копію (pure update)."""
        return replace(self, tags=self.tags | frozenset({tag}))

    def with_item(self, item: Item) -> Order:
        """Додає товар, повертаючи нову копію (pure update)."""
        return replace(self, items=self.items + (item,))

    def mark_as_paid(self) -> Order:
        """Змінює статус оплати, повертаючи нову копію (pure update)."""
        return replace(self, paid=True)
