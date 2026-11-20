from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, status, Query
from pydantic import BaseModel
from ..models import Product, ProductCreate, Order, OrderStatusUpdate
from ..services.firestore_service import FirestoreService
from ..security import require_admin

router = APIRouter(prefix="/admin", tags=["Admin Portal"])

class ProductUpdateRequest(BaseModel):
    title: Optional[str] = None
    name: Optional[str] = None
    subtitle: Optional[str] = None
    category: Optional[str] = None
    price: Optional[str] = None
    numericPrice: Optional[float] = None
    image: Optional[str] = None
    frontImage: Optional[str] = None
    sideImage: Optional[str] = None
    tag: Optional[str] = None
    desc: Optional[str] = None
    sizes: Optional[List[str]] = None
    in_stock: Optional[bool] = None

class PaymentVerificationRequest(BaseModel):
    status: str = "VERIFIED" # VERIFIED or FAILED
    notes: Optional[str] = None

# =============================================================================
# DASHBOARD OVERVIEW & ANALYTICS
# =============================================================================

@router.get("/overview")
def get_dashboard_overview(admin: Dict[str, Any] = Depends(require_admin)):
    """Retrieve real-time executive dashboard metrics from Firestore database."""
    metrics = FirestoreService.get_admin_dashboard_metrics()
    recent_orders = FirestoreService.list_orders_admin(limit=10)
    recent_logs = FirestoreService.get_admin_logs(limit=5)
    return {
        "metrics": metrics,
        "recent_orders": recent_orders,
        "recent_logs": recent_logs,
        "admin": {
            "email": admin.get("email"),
            "name": admin.get("name")
        }
    }

# =============================================================================
# ORDER MANAGEMENT
# =============================================================================

@router.get("/orders", response_model=List[Order])
def get_all_orders(
    status: Optional[str] = Query(None, description="Filter by order status"),
    search: Optional[str] = Query(None, description="Search by Order ID, customer, or reference"),
    limit: int = Query(100, le=500),
    admin: Dict[str, Any] = Depends(require_admin)
):
    """List all orders with status filtering and text search."""
    return FirestoreService.list_orders_admin(status=status, search=search, limit=limit)

@router.get("/orders/{order_id}", response_model=Order)
def get_admin_order(order_id: str, admin: Dict[str, Any] = Depends(require_admin)):
    """Retrieve complete details for a specific order."""
    order = FirestoreService.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")
    return order

@router.patch("/orders/{order_id}/status", response_model=Order)
def update_order_status(
    order_id: str,
    payload: OrderStatusUpdate,
    admin: Dict[str, Any] = Depends(require_admin)
):
    """
    Update workflow status for an order:
    CONFIRMED -> PROCESSING -> PACKED -> SHIPPED -> OUT_FOR_DELIVERY -> DELIVERED,
    or CANCELLED / REFUNDED.
    """
    updated = FirestoreService.update_order_status(
        order_id=order_id,
        new_status=payload.status,
        notes=payload.notes,
        tracking_number=payload.tracking_number,
        payment_status=payload.payment_status,
        updated_by=admin.get("email")
    )
    if not updated:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found.")
    return updated

# =============================================================================
# PRODUCT & INVENTORY MANAGEMENT
# =============================================================================

@router.get("/products", response_model=List[Product])
def list_admin_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    admin: Dict[str, Any] = Depends(require_admin)
):
    """List all products in catalog."""
    return FirestoreService.get_all_products(category=category, search=search)

@router.post("/products", response_model=Product, status_code=201)
def create_product(product: ProductCreate, admin: Dict[str, Any] = Depends(require_admin)):
    """Create a new product in the catalog."""
    new_prod = FirestoreService.add_product(product.model_dump())
    FirestoreService.log_admin_action(admin["email"], f"Created product: {new_prod.id}")
    return new_prod

@router.put("/products/{product_id}", response_model=Product)
@router.patch("/products/{product_id}", response_model=Product)
def update_product(
    product_id: str,
    payload: ProductUpdateRequest,
    admin: Dict[str, Any] = Depends(require_admin)
):
    """Update existing product details, pricing, sizes, or stock status."""
    if payload.numericPrice is not None and payload.numericPrice <= 0:
        raise HTTPException(status_code=400, detail="Product price must be greater than zero.")
    updated = FirestoreService.update_product(product_id, payload.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found.")
    FirestoreService.log_admin_action(admin["email"], f"Updated product: {product_id}")
    return updated

@router.delete("/products/{product_id}")
def delete_product(product_id: str, admin: Dict[str, Any] = Depends(require_admin)):
    """Remove a product from the catalog."""
    success = FirestoreService.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found.")
    FirestoreService.log_admin_action(admin["email"], f"Deleted product: {product_id}")
    return {"message": f"Product '{product_id}' deleted successfully."}

# =============================================================================
# CUSTOMERS DIRECTORY
# =============================================================================

@router.get("/customers")
def list_customers(
    limit: int = Query(100, le=500),
    admin: Dict[str, Any] = Depends(require_admin)
):
    """List registered customers with order summary information."""
    users = FirestoreService.list_users(limit=limit, role="CUSTOMER")
    orders = FirestoreService.list_orders_admin(limit=1000)

    # Compute order stats per customer
    order_counts = {}
    total_spent = {}
    for o in orders:
        email = o.customer_email.lower().strip()
        order_counts[email] = order_counts.get(email, 0) + 1
        if o.status.upper() not in ["CANCELLED", "PAYMENT_FAILED"]:
            total_spent[email] = total_spent.get(email, 0.0) + float(o.total)

    enriched_customers = []
    for u in users:
        email = u.get("email", "").lower()
        enriched_customers.append({
            "user_id": u.get("user_id"),
            "name": u.get("name"),
            "email": u.get("email"),
            "phone": u.get("phone"),
            "created_at": u.get("created_at"),
            "orders_count": order_counts.get(email, 0),
            "total_spent": round(total_spent.get(email, 0.0), 2),
            "tier": "VIP" if order_counts.get(email, 0) > 2 else "Member"
        })

    return enriched_customers

# =============================================================================
# PAYMENTS & RECONCILIATION
# =============================================================================

@router.get("/payments")
def list_payments(
    status: Optional[str] = None,
    order_id: Optional[str] = None,
    admin: Dict[str, Any] = Depends(require_admin)
):
    """List payments with verification status."""
    return FirestoreService.get_payments(order_id=order_id, status=status)

@router.post("/payments/{payment_id}/verify")
def verify_payment_transaction(
    payment_id: str,
    payload: PaymentVerificationRequest,
    admin: Dict[str, Any] = Depends(require_admin)
):
    """
    Admin action: Verify or reject payment transaction after checking bank statement/UPI app.
    Updates the payment and automatically confirms or fails the associated order.
    """
    updated_payment = FirestoreService.verify_payment(
        payment_id=payment_id,
        verified_by=admin["email"],
        status=payload.status
    )
    if not updated_payment:
        raise HTTPException(status_code=404, detail=f"Payment '{payment_id}' not found.")
    return {"message": f"Payment {payment_id} marked as {payload.status}.", "payment": updated_payment}

# =============================================================================
# AUDIT LOGS
# =============================================================================

@router.get("/logs")
def get_activity_logs(limit: int = 50, admin: Dict[str, Any] = Depends(require_admin)):
    """Retrieve recent admin activity logs."""
    return FirestoreService.get_admin_logs(limit=limit)
