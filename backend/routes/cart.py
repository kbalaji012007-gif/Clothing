from fastapi import APIRouter, HTTPException
from ..models import Cart, AddToCartRequest
from ..services.firestore_service import FirestoreService

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/{session_id}", response_model=Cart)
def get_cart(session_id: str):
    """Get the active shopping bag / cart for a user session."""
    return FirestoreService.get_cart(session_id)

@router.post("/{session_id}/items", response_model=Cart)
def add_item_to_cart(session_id: str, payload: AddToCartRequest):
    """Add a product (with size and quantity) to the user's shopping bag."""
    try:
        return FirestoreService.add_to_cart(
            session_id=session_id,
            product_id=payload.product_id,
            size=payload.size,
            quantity=payload.quantity
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{session_id}/items/{item_id}", response_model=Cart)
def remove_item_from_cart(session_id: str, item_id: str):
    """Remove a specific line item from the shopping bag."""
    return FirestoreService.remove_from_cart(session_id, item_id)

@router.delete("/{session_id}", response_model=Cart)
def clear_cart(session_id: str):
    """Clear all items from the user's shopping bag."""
    return FirestoreService.clear_cart(session_id)
