from typing import List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class OrderItem(BaseModel):
    product_id: str
    title: str
    size: str = "M"
    color: Optional[str] = None
    quantity: int = 1
    price: float = 0.0
    image: Optional[str] = None

class OrderCreate(BaseModel):
    customer_id: Optional[str] = None
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    shipping_address: str
    session_id: Optional[str] = None
    items: List[OrderItem] = Field(default_factory=list)
    payment_method: str = "card"
    payment_reference: Optional[str] = None
    delivery_charge: float = 0.0
    discount: float = 0.0
    notes: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = None
    tracking_number: Optional[str] = None
    payment_status: Optional[str] = None

class OrderCancellationRequest(BaseModel):
    reason: str

class OrderRefundRequest(BaseModel):
    reason: str

class Order(BaseModel):
    id: str
    customer_id: Optional[str] = None
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    shipping_address: str
    items: List[OrderItem]
    subtotal: float
    tax: float = 0.0
    delivery_charge: float = 0.0
    discount: float = 0.0
    total: float
    payment_method: str = "card"
    payment_reference: Optional[str] = None
    payment_status: str = "PENDING"  # PENDING, UNDER_REVIEW, VERIFIED, FAILED, REFUNDED
    status: str = "CONFIRMED"        # PAYMENT_PENDING, PAYMENT_UNDER_REVIEW, CONFIRMED, PROCESSING, PACKED, SHIPPED, OUT_FOR_DELIVERY, DELIVERED, CANCELLED, REFUND_REQUESTED, REFUNDED
    tracking_number: Optional[str] = None
    cancellation_reason: Optional[str] = None
    refund_reason: Optional[str] = None
    admin_notes: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: Optional[str] = None
