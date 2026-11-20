from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Depends, Response
from ..models import Product, ProductCreate, ProductUpdateRequest
from ..services.firestore_service import FirestoreService
from ..security import require_admin

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=List[Product])
def list_products(
    response: Response,
    category: Optional[str] = Query(None, description="Filter by category: 'sneakers', 'rack', 'runway'"),
    search: Optional[str] = Query(None, description="Search term for title, name, or description")
):
    """Retrieve all store products with optional category and search filters."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return FirestoreService.get_all_products(category=category, search=search)

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: str, response: Response):
    """Retrieve a single product by its unique identifier."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    product = FirestoreService.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found.")
    return product

@router.post("", response_model=Product, status_code=201)
def create_product(product: ProductCreate, admin: Dict[str, Any] = Depends(require_admin)):
    """Create or register a new product in Firestore (Admin only)."""
    if product.numericPrice <= 0:
        raise HTTPException(status_code=400, detail="Product price must be greater than zero.")
    return FirestoreService.add_product(product.model_dump())

@router.put("/{product_id}", response_model=Product)
@router.patch("/{product_id}", response_model=Product)
def update_product_endpoint(
    product_id: str,
    payload: ProductUpdateRequest,
    admin: Dict[str, Any] = Depends(require_admin)
):
    """Update existing product details, pricing, sizes, or stock status (Admin only)."""
    if payload.numericPrice is not None and payload.numericPrice <= 0:
        raise HTTPException(status_code=400, detail="Product price must be greater than zero.")
    updated = FirestoreService.update_product(product_id, payload.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found.")
    FirestoreService.log_admin_action(admin["email"], f"Updated product: {product_id}")
    return updated
