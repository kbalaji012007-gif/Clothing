from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class OrderItem(BaseModel):
    product_id: str
    title: str
    size: str
    quantity: int
    price: float

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    shipping_address: str
    session_id: Optional[str] = None
    items: List[OrderItem] = Field(default_factory=list)
    payment_method: str = "card"

class Order(BaseModel):
    id: str
    customer_name: str
    customer_email: str
    shipping_address: str
    items: List[OrderItem]
    subtotal: float
    total: float
    payment_method: str = "card"
    status: str = "confirmed"  # pending, confirmed, shipped, delivered
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
