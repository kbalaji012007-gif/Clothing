from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from ..models import Product, ProductCreate
from ..services.firestore_service import FirestoreService

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=List[Product])
def list_products(
    category: Optional[str] = Query(None, description="Filter by category: 'sneakers', 'rack', 'runway'"),
    search: Optional[str] = Query(None, description="Search term for title, name, or description")
):
    """Retrieve all store products with optional category and search filters."""
    return FirestoreService.get_all_products(category=category, search=search)

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: str):
    """Retrieve a single product by its unique identifier."""
    product = FirestoreService.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found.")
    return product

@router.post("", response_model=Product, status_code=201)
def create_product(product: ProductCreate):
    """Create or register a new product in Firestore."""
    return FirestoreService.add_product(product.model_dump())
