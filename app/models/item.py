# Sample Pydantic model
from pydantic import BaseModel # type: ignore

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
