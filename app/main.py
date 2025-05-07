from typing import Annotated

from fastapi import FastAPI, HTTPException, Query

from app.crud import create_item, get_items, update_item_by_id
from app.models import Item, ItemCreate, ItemUpdate, FilterParameters

app = FastAPI()


# 1 corrected the spelling of the endpoint
# health was misspelled as heath
@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


# 4 added an offset and limit so fewer data is sent through the network at a time
@app.get("/items")
def list_items(query: Annotated[FilterParameters, Query()]) -> list[Item]:
    if query.min_price < 0:
        raise HTTPException(status_code=400, detail="Price cannot be negative.")
    if query.offset < 0:
        raise HTTPException(status_code=400, detail="Offset cannot be negative.")
    if query.limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be greater than zero.")
    return get_items(min_price=query.min_price, offset=query.offset, limit=query.limit)


@app.post("/items")
def add_item(item: ItemCreate) -> Item:
    new_item = create_item(item)
    if new_item == "duplicate_name":
        raise HTTPException(status_code=400, detail="Duplicate Name")
    return new_item


# If the name is already being used the server sends a 422 response
@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate) -> Item:
    updated = update_item_by_id(item_id, item)
    if updated == "duplicate_name":
        raise HTTPException(status_code=400, detail="Duplicate Name")
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated
