from typing import List

from app.database import items_db
from app.models import Item, ItemCreate, ItemUpdate


#2 Fixed logic issue where the function was returning items with a
# lower price than the minimum instead of higher
# only iterates through the items in the range offset until offset + limit
def get_items(min_price: float = 0.0, offset: int = 0, limit: int = 100) -> List[Item]:
    return [Item(**item) for item in items_db[offset: offset + limit] if item["price"] >= min_price]


def create_item(item: ItemCreate) -> Item | str:
    duplicate = sum(1 for i in items_db if item.name == i["name"])
    if duplicate > 0:
        return "duplicate_name"
    new_id = len(items_db)
    new_item = {"id": new_id, **item.model_dump()}
    items_db.append(new_item)
    return Item(**new_item)


#4 added verification for duplicate names
def update_item_by_id(item_id: int, update: ItemUpdate) -> Item | str | None:
    if update.name:
        for item in items_db:
            if update.name == item["name"]:
                return "duplicate_name"
    for item in items_db:
        if item["id"] == item_id:
            if update.name:
                item["name"] = update.name
            if update.price:
                item["price"] = update.price
            return Item(**item)
    return None
