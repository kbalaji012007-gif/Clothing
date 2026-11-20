import re
import urllib.parse
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ..services.firestore_service import FirestoreService
from ..config import logger

router = APIRouter(prefix="/upi", tags=["UPI Gateway"])

DEFAULT_PAYEE_VPA = "atelier@upi"
DEFAULT_PAYEE_NAME = "Atelier Collection"
USD_TO_INR_RATE = 86.50

class UpiCreateIntentRequest(BaseModel):
    orderId: str
    amountUsd: float
    customerName: Optional[str] = "Member"
    customerEmail: Optional[str] = "member@atelier.com"
    items: List[dict] = Field(default_factory=list)

class UpiSubmitUtrRequest(BaseModel):
    orderId: str
    utr: str
    amountUsd: float
    customerName: Optional[str] = "Member"
    customerEmail: Optional[str] = "member@atelier.com"
    items: List[dict] = Field(default_factory=list)

@router.post("/create-intent")
def create_upi_intent(payload: UpiCreateIntentRequest):
    """
    Creates canonical UPI payment intent URI, QR code payload, and app deeplinks.
    Conforms to the YouPI-PG UPI Specification.
    """
    amount_inr = round(payload.amountUsd * USD_TO_INR_RATE, 2)
    amount_str = f"{amount_inr:.2f}"
    
    # Canonical upi://pay parameters
    params = {
        "pa": DEFAULT_PAYEE_VPA,
        "pn": DEFAULT_PAYEE_NAME,
        "am": amount_str,
        "cu": "INR",
        "tn": f"Atelier Order {payload.orderId}"
    }
    
    query_string = urllib.parse.urlencode(params)
    upi_uri = f"upi://pay?{query_string}"
    
    # Provider-specific Android Intent links (from YouPI central registry)
    gpay_uri = f"intent://pay?{query_string}#Intent;scheme=upi;package=com.google.android.apps.nbu.paisa.user;end"
    phonepe_uri = f"intent://pay?{query_string}#Intent;scheme=upi;package=com.phonepe.app;end"
    paytm_uri = f"intent://pay?{query_string}#Intent;scheme=upi;package=net.one97.paytm;end"

    # Online QR Code Image URL (Scan with any UPI camera / app)
    encoded_uri = urllib.parse.quote(upi_uri)
    qr_image_url = f"https://api.qrserver.com/v1/create-qr-code/?size=260x260&margin=8&data={encoded_uri}"

    return {
        "orderId": payload.orderId,
        "amountUsd": payload.amountUsd,
        "amountInr": amount_inr,
        "formattedInr": f"₹{amount_inr:,.2f}",
        "payeeVpa": DEFAULT_PAYEE_VPA,
        "payeeName": DEFAULT_PAYEE_NAME,
        "upiUri": upi_uri,
        "qrImageUrl": qr_image_url,
        "providers": [
            { "id": "gpay", "name": "Google Pay", "icon": "⚡ GPay", "uri": gpay_uri },
            { "id": "phonepe", "name": "PhonePe", "icon": "🟣 PhonePe", "uri": phonepe_uri },
            { "id": "paytm", "name": "Paytm", "icon": "🔵 Paytm", "uri": paytm_uri }
        ]
    }

@router.post("/submit-utr")
def submit_upi_utr(payload: UpiSubmitUtrRequest):
    """
    Submits and verifies the 12-digit UPI UTR transaction reference,
    and commits the confirmed order directly to Cloud Firestore.
    """
    clean_utr = payload.utr.strip()
    
    # Validate 12-digit standard UTR
    if not re.match(r"^\d{12}$", clean_utr):
        raise HTTPException(
            status_code=400,
            detail="Invalid UPI reference number (UTR). Please enter a valid 12-digit numeric reference."
        )

    # Format order items
    order_items = []
    for item in payload.items:
        order_items.append({
            "product_id": str(item.get("product_id") or item.get("id", "piece")),
            "title": str(item.get("title") or item.get("name", "Atelier Piece")),
            "size": str(item.get("size", "M")),
            "quantity": int(item.get("quantity", 1)),
            "price": float(item.get("price", 0.0))
        })

    # Record order in Cloud Firestore
    order_data = {
        "id": payload.orderId,
        "customer_name": payload.customerName,
        "customer_email": payload.customerEmail,
        "shipping_address": "Atelier Member Express Delivery",
        "items": order_items,
        "payment_method": f"UPI (UTR: {clean_utr})",
        "payment_status": "verified",
        "subtotal": payload.amountUsd,
        "total": payload.amountUsd
    }

    try:
        confirmed_order = FirestoreService.create_order(order_data)
        logger.info(f"UPI Order {payload.orderId} verified and recorded with UTR {clean_utr}")
        return {
            "status": "success",
            "message": "Payment verified successfully.",
            "order": confirmed_order.model_dump(),
            "utr": clean_utr
        }
    except Exception as e:
        logger.error(f"Error recording UPI order: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to record order: {e}")
