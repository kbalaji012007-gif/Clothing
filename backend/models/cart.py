from typing import List, Optional
from pydantic import BaseModel, Field

class CartItem(BaseModel):
    item_id: str
    product_id: str
    title: str
    size: str = "M"
    quantity: int = 1
    price: float = 0.0
    price_formatted: str = "$0.00"
    image: Optional[str] = None

class Cart(BaseModel):
    session_id: str
    items: List[CartItem] = Field(default_factory=list)
    subtotal: float = 0.0
    subtotal_formatted: str = "$0.00"
    total_items: int = 0

class AddToCartRequest(BaseModel):
    product_id: str
    size: str = "M"
    quantity: int = 1
