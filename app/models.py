from typing import Optional

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int
    name: str
    price: float


# 3 enforced a minimum of three characters directly in base model
# non compliance will result in 422 response

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=3)
    price: float = Field(ge=0)


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

class FilterParameters(BaseModel):
    model_config = {"extra": "forbid"}
    min_price: float = Field(0.0)
    offset: int = Field(0)
    limit: int = Field(100)
