from .products import router as products_router
from .cart import router as cart_router
from .orders import router as orders_router
from .auth import router as auth_router
from .upi import router as upi_router

__all__ = ["products_router", "cart_router", "orders_router", "auth_router", "upi_router"]
