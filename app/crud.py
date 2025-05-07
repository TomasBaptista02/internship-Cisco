from typing import List

from app.database import items_db
from app.models import Item, ItemCreate, ItemUpdate

#2 Fixed logic issue where the function was returning items with a
# lower price than the minimum instead of higher
def get_items(min_price: float = 0.0) -> List[Item]:
    return [Item(**item) for item in items_db if item["price"] >= min_price]


def create_item(item: ItemCreate) -> Item:
    new_id = max(item["id"] for item in items_db) + 1
    new_item = {"id": new_id, **item.dict()}
    items_db.append(new_item)
    return Item(**new_item)


def update_item_by_id(item_id: int, update: ItemUpdate) -> Item | None:
    for item in items_db:
        if item["id"] == item_id:
            if update.name:
                item["name"] = update.name
            if update.price:
                item["price"] = update.price
            return Item(**item)
    return None
