from collections.abc import Mapping, Sequence

from model import Item, Order


def add_vip_tag(o: Order) -> Order:
    """Додає тег 'vip' до замовлення без мутації оригіналу."""
    return o.add_tag("vip")


def add_item_to_order(o: Order, sku: str, price: float, qty: int) -> Order:
    """Додає новий товар до замовлення без мутації оригіналу."""
    return o.with_item(Item(sku=sku, price=price, qty=qty))


def top_expensive_items(items: Sequence[Item], n: int = 3) -> tuple[Item, ...]:
    """Повертає топ найдорожчих товарів у вигляді tuple."""
    return tuple(sorted(items, key=lambda i: i.price * i.qty, reverse=True)[:n])


def get_source(meta: Mapping[str, str]) -> str:
    """Безпечне читання з read-only словника."""
    return meta.get("source", "unknown")
