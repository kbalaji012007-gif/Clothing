import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from ..config import get_firestore_client, logger
from ..models import Product, Cart, CartItem, Order, OrderItem

from database.seed_data import INITIAL_SEED_PRODUCTS

class FirestoreService:
    # In-memory store used when Firebase credentials are not provided
    _memory_products: Dict[str, Dict[str, Any]] = {p["id"]: dict(p) for p in INITIAL_SEED_PRODUCTS}
    _memory_carts: Dict[str, Dict[str, Any]] = {}
    _memory_orders: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def seed_products_if_empty(cls):
        """Populates the Firestore 'products' collection if empty."""
        db = get_firestore_client()
        if not db:
            logger.info("Firestore client not connected. In-memory products store populated with %d items.", len(cls._memory_products))
            return len(cls._memory_products)

        try:
            products_ref = db.collection("products")
            docs = list(products_ref.limit(1).stream())
            if not docs:
                logger.info("Firestore 'products' collection is empty. Seeding %d initial items...", len(INITIAL_SEED_PRODUCTS))
                batch = db.batch()
                for prod in INITIAL_SEED_PRODUCTS:
                    doc_ref = products_ref.document(prod["id"])
                    batch.set(doc_ref, prod)
                batch.commit()
                logger.info("Successfully seeded products into Firestore.")
            else:
                logger.info("Firestore 'products' collection already contains data.")
            return len(INITIAL_SEED_PRODUCTS)
        except Exception as e:
            logger.error(f"Error seeding products to Firestore: {e}")
            return len(cls._memory_products)

    @classmethod
    def get_all_products(cls, category: Optional[str] = None, search: Optional[str] = None) -> List[Product]:
        db = get_firestore_client()
        products_data = []

        if db:
            try:
                ref = db.collection("products")
                if category:
                    ref = ref.where("category", "==", category)
                docs = ref.stream()
                for doc in docs:
                    data = doc.to_dict()
                    data["id"] = doc.id
                    products_data.append(data)
            except Exception as e:
                logger.warning(f"Error fetching products from Firestore: {e}. Falling back to memory.")
                products_data = list(cls._memory_products.values())
        else:
            products_data = list(cls._memory_products.values())

        # In-memory filtering for category & search
        results = []
        for p in products_data:
            if category and p.get("category") != category:
                continue
            if search:
                s_lower = search.lower()
                title_match = s_lower in p.get("title", "").lower()
                name_match = s_lower in p.get("name", "").lower()
                desc_match = s_lower in p.get("desc", "").lower()
                if not (title_match or name_match or desc_match):
                    continue
            results.append(Product(**p))

        return results

    @classmethod
    def get_product(cls, product_id: str) -> Optional[Product]:
        db = get_firestore_client()
        if db:
            try:
                doc = db.collection("products").document(product_id).get()
                if doc.exists:
                    data = doc.to_dict()
                    data["id"] = doc.id
                    return Product(**data)
            except Exception as e:
                logger.warning(f"Error getting product {product_id} from Firestore: {e}")

        if product_id in cls._memory_products:
            return Product(**cls._memory_products[product_id])
        return None

    @classmethod
    def add_product(cls, product_data: Dict[str, Any]) -> Product:
        pid = product_data.get("id") or str(uuid.uuid4())
        product_data["id"] = pid
        db = get_firestore_client()
        if db:
            try:
                db.collection("products").document(pid).set(product_data)
            except Exception as e:
                logger.warning(f"Error adding product to Firestore: {e}")

        cls._memory_products[pid] = dict(product_data)
        return Product(**product_data)

    # --- Cart Management ---

    @classmethod
    def get_cart(cls, session_id: str) -> Cart:
        db = get_firestore_client()
        if db:
            try:
                doc = db.collection("carts").document(session_id).get()
                if doc.exists:
                    data = doc.to_dict()
                    return Cart(**data)
            except Exception as e:
                logger.warning(f"Error getting cart from Firestore: {e}")

        if session_id not in cls._memory_carts:
            cls._memory_carts[session_id] = {
                "session_id": session_id,
                "items": [],
                "subtotal": 0.0,
                "subtotal_formatted": "$0.00",
                "total_items": 0
            }
        return Cart(**cls._memory_carts[session_id])

    @classmethod
    def add_to_cart(cls, session_id: str, product_id: str, size: str = "M", quantity: int = 1) -> Cart:
        product = cls.get_product(product_id)
        if not product:
            raise ValueError(f"Product '{product_id}' not found.")

        cart = cls.get_cart(session_id)
        items = list(cart.items)

        # Check if identical product + size already in cart
        found = False
        for item in items:
            if item.product_id == product_id and item.size == size:
                item.quantity += quantity
                found = True
                break

        if not found:
            new_item = CartItem(
                item_id=str(uuid.uuid4())[:8],
                product_id=product.id,
                title=product.title,
                size=size,
                quantity=quantity,
                price=product.numericPrice,
                price_formatted=product.price,
                image=product.image or product.frontImage
            )
            items.append(new_item)

        subtotal = sum(i.price * i.quantity for i in items)
        total_items = sum(i.quantity for i in items)

        updated_cart = Cart(
            session_id=session_id,
            items=items,
            subtotal=round(subtotal, 2),
            subtotal_formatted=f"${subtotal:.2f}",
            total_items=total_items
        )

        db = get_firestore_client()
        if db:
            try:
                db.collection("carts").document(session_id).set(updated_cart.model_dump())
            except Exception as e:
                logger.warning(f"Error updating cart in Firestore: {e}")

        cls._memory_carts[session_id] = updated_cart.model_dump()
        return updated_cart

    @classmethod
    def remove_from_cart(cls, session_id: str, item_id: str) -> Cart:
        cart = cls.get_cart(session_id)
        items = [i for i in cart.items if i.item_id != item_id]
        subtotal = sum(i.price * i.quantity for i in items)
        total_items = sum(i.quantity for i in items)

        updated_cart = Cart(
            session_id=session_id,
            items=items,
            subtotal=round(subtotal, 2),
            subtotal_formatted=f"${subtotal:.2f}",
            total_items=total_items
        )

        db = get_firestore_client()
        if db:
            try:
                db.collection("carts").document(session_id).set(updated_cart.model_dump())
            except Exception as e:
                logger.warning(f"Error updating cart in Firestore: {e}")

        cls._memory_carts[session_id] = updated_cart.model_dump()
        return updated_cart

    @classmethod
    def clear_cart(cls, session_id: str) -> Cart:
        empty_cart = Cart(
            session_id=session_id,
            items=[],
            subtotal=0.0,
            subtotal_formatted="$0.00",
            total_items=0
        )
        db = get_firestore_client()
        if db:
            try:
                db.collection("carts").document(session_id).set(empty_cart.model_dump())
            except Exception as e:
                logger.warning(f"Error clearing cart in Firestore: {e}")

        cls._memory_carts[session_id] = empty_cart.model_dump()
        return empty_cart

    # --- Orders & Checkout ---

    @classmethod
    def create_order(cls, order_data: Dict[str, Any]) -> Order:
        order_id = order_data.get("id") or f"ORD-{uuid.uuid4().hex[:8].upper()}"
        items_raw = order_data.get("items", [])
        items = [OrderItem(**i) if isinstance(i, dict) else i for i in items_raw]
        subtotal = sum(i.price * i.quantity for i in items)

        order = Order(
            id=order_id,
            customer_name=order_data.get("customer_name", "Anonymous"),
            customer_email=order_data.get("customer_email", ""),
            shipping_address=order_data.get("shipping_address", ""),
            items=items,
            subtotal=round(subtotal, 2),
            total=round(subtotal, 2),
            payment_method=order_data.get("payment_method", "card"),
            status="confirmed",
            created_at=datetime.utcnow().isoformat()
        )

        db = get_firestore_client()
        if db:
            try:
                db.collection("orders").document(order_id).set(order.model_dump())
                logger.info(f"Order {order_id} saved to Firestore.")
            except Exception as e:
                logger.warning(f"Error saving order to Firestore: {e}")

        cls._memory_orders[order_id] = order.model_dump()

        # Clear cart if session_id provided
        session_id = order_data.get("session_id")
        if session_id:
            cls.clear_cart(session_id)

        return order

    @classmethod
    def get_order(cls, order_id: str) -> Optional[Order]:
        db = get_firestore_client()
        if db:
            try:
                doc = db.collection("orders").document(order_id).get()
                if doc.exists:
                    return Order(**doc.to_dict())
            except Exception as e:
                logger.warning(f"Error getting order from Firestore: {e}")

        if order_id in cls._memory_orders:
            return Order(**cls._memory_orders[order_id])
        return None

    @classmethod
    def list_orders(cls) -> List[Order]:
        db = get_firestore_client()
        if db:
            try:
                docs = db.collection("orders").order_by("created_at", direction="DESCENDING").limit(50).stream()
                return [Order(**doc.to_dict()) for doc in docs]
            except Exception as e:
                logger.warning(f"Error listing orders from Firestore: {e}")

        return [Order(**o) for o in cls._memory_orders.values()]
