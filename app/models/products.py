from pydantic import BaseModel
from typing import Optional


class Products(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    stock: int
