import re
import uuid
import urllib.parse
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
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
    Validates item prices against authoritative Firestore catalog to reject price manipulation.
    """
    if payload.items:
        expected = 0.0
        for itm in payload.items:
            pid = str(itm.get("product_id") or itm.get("id") or "")
            p = FirestoreService.get_product(pid)
            if p:
                expected += p.numericPrice * int(itm.get("quantity", 1))
            else:
                raise HTTPException(status_code=400, detail=f"Product '{pid}' not found in catalog.")
        if expected > 0 and abs(payload.amountUsd - expected) > 0.01:
            raise HTTPException(
                status_code=400,
                detail=f"Price manipulation detected: provided amount {payload.amountUsd} does not match catalog subtotal {expected}."
            )

    is_inr = payload.amountUsd >= 500 or any(float(i.get("price", 0)) >= 500 for i in payload.items)
    amount_inr = round(payload.amountUsd, 2) if is_inr else round(payload.amountUsd * USD_TO_INR_RATE, 2)
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
    Submits the 12-digit UPI UTR transaction reference for review.
    Enforces format validation, prevents duplicate UTR reuse, records a payment transaction,
    and sets status to PAYMENT_UNDER_REVIEW pending administrative verification.
    """
    clean_utr = payload.utr.strip()
    
    # 1. Validate 12-digit standard numeric UTR
    if not re.match(r"^\d{12}$", clean_utr):
        raise HTTPException(
            status_code=400,
            detail="Invalid UPI reference number (UTR). Please enter a valid 12-digit numeric reference."
        )

    # 2. Prevent duplicate UTR submission
    if FirestoreService.check_duplicate_utr(clean_utr):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This 12-digit UTR reference has already been submitted for another order. Duplicate payments are not accepted."
        )

    # 3. Check duplicate order
    existing_order = FirestoreService.get_order(payload.orderId)
    if existing_order and existing_order.status.upper() in ["CONFIRMED", "PROCESSING", "SHIPPED", "DELIVERED"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Order '{payload.orderId}' has already been confirmed."
        )

    # 4. Format order items
    order_items = []
    for item in payload.items:
        order_items.append({
            "product_id": str(item.get("product_id") or item.get("id", "piece")),
            "title": str(item.get("title") or item.get("name", "Atelier Piece")),
            "size": str(item.get("size", "M")),
            "color": item.get("color"),
            "quantity": int(item.get("quantity", 1)),
            "price": float(item.get("price", 0.0)),
            "image": item.get("image")
        })

    # 5. Record Payment transaction
    is_inr = payload.amountUsd >= 500 or any(float(i.get("price", 0)) >= 500 for i in payload.items)
    payment_amount_inr = round(payload.amountUsd, 2) if is_inr else round(payload.amountUsd * USD_TO_INR_RATE, 2)
    payment_id = f"PAY-{uuid.uuid4().hex[:8].upper()}"
    payment_record = {
        "payment_id": payment_id,
        "order_id": payload.orderId,
        "amount": payment_amount_inr,
        "currency": "INR",
        "amount_usd": payload.amountUsd,
        "payment_method": "UPI",
        "utr_reference": clean_utr,
        "status": "UNDER_REVIEW",
        "customer_email": payload.customerEmail,
        "customer_name": payload.customerName,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    FirestoreService.record_payment(payment_record)

    # 6. Record order in Cloud Firestore with PAYMENT_UNDER_REVIEW status
    order_data = {
        "id": payload.orderId,
        "customer_name": payload.customerName,
        "customer_email": payload.customerEmail,
        "shipping_address": "Atelier Member Express Delivery",
        "items": order_items,
        "payment_method": f"UPI (UTR: {clean_utr})",
        "payment_reference": clean_utr,
        "payment_status": "UNDER_REVIEW",
        "status": "PAYMENT_UNDER_REVIEW",
        "subtotal": payload.amountUsd,
        "total": payload.amountUsd
    }

    try:
        created_order = FirestoreService.create_order(order_data)
        logger.info(f"UPI Order {payload.orderId} submitted with UTR {clean_utr} (status: PAYMENT_UNDER_REVIEW)")
        return {
            "status": "under_review",
            "message": "Payment submitted successfully. Your transaction is under review by Atelier treasury.",
            "order": created_order.model_dump(),
            "payment_id": payment_id,
            "utr": clean_utr
        }
    except ValueError as e:
        logger.warning(f"Price validation failed in UPI order: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error recording UPI order: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to record order: {e}")
