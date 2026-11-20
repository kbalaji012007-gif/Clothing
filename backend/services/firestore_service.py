import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from ..config import get_firestore_client, logger
from ..models import Product, Cart, CartItem, Order, OrderItem

from database.seed_data import INITIAL_SEED_PRODUCTS

PRODUCT_ALIASES = {
    "blazer-navy": "rack-blazer-navy-1",
    "hoodie-graphic": "rack-hoodie-grey-1",
    "hoodie-heavy": "rack-hoodie-black-1",
    "hoodie-fleece": "rack-hoodie-cream-1",
    "crew-minimal": "rack-crew-ash-1",
    "runway-tee": "runway-tshirt",
    "tshirt": "runway-tshirt",
    "runway-sweat": "runway-sweatshirt",
    "sweatshirt": "runway-sweatshirt",
    "runway-sweat-plus": "runway-sweatshirt-plus",
    "sweatshirt-plus": "runway-sweatshirt-plus",
    "hoodie-black": "rack-hoodie-black-1",
    "hoodie": "rack-hoodie-grey-1",
    "tatum-5-orbit-copy": "tatum-5-orbit",
    "air-jordan-12-retro-copy": "luka-5",
}

class FirestoreService:
    # In-memory stores used when Firebase credentials are not provided
    _memory_products: Dict[str, Dict[str, Any]] = {p["id"]: dict(p) for p in INITIAL_SEED_PRODUCTS}
    _memory_carts: Dict[str, Dict[str, Any]] = {}
    _memory_orders: Dict[str, Dict[str, Any]] = {}
    _memory_users: Dict[str, Dict[str, Any]] = {}
    _memory_payments: Dict[str, Dict[str, Any]] = {}
    _memory_admin_logs: List[Dict[str, Any]] = []

    # =========================================================================
    # PRODUCTS & CATALOG
    # =========================================================================

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
        canonical_id = PRODUCT_ALIASES.get(product_id, product_id)
        
        # Build candidate IDs to resolve cart variations, sizes, and prefixes
        possible_ids = [canonical_id, product_id]
        clean_id = product_id
        if clean_id.startswith("orbit-"):
            clean_id = clean_id[len("orbit-"):]
        elif clean_id.startswith("rack-"):
            pass
        parts = clean_id.rsplit("-", 1)
        if len(parts) == 2 and parts[1].upper() in ["S", "M", "L", "XL", "XXL", "40", "41", "42", "43", "44", "45", "46"]:
            possible_ids.append(parts[0])
            if parts[0] in PRODUCT_ALIASES:
                possible_ids.append(PRODUCT_ALIASES[parts[0]])
        possible_ids.append(clean_id)

        db = get_firestore_client()
        if db:
            for pid in possible_ids:
                try:
                    doc = db.collection("products").document(pid).get()
                    if doc.exists:
                        data = doc.to_dict()
                        data["id"] = doc.id
                        return Product(**data)
                except Exception as e:
                    logger.warning(f"Error getting product {pid} from Firestore: {e}")

        for pid in possible_ids:
            if pid in cls._memory_products:
                return Product(**cls._memory_products[pid])

        # Substring / fuzzy match fallback against all in-memory products
        for p in cls._memory_products.values():
            pid = p.get("id", "")
            if pid and (pid == clean_id or pid in product_id or clean_id in pid):
                return Product(**p)

        return None

    @classmethod
    def add_product(cls, product_data: Dict[str, Any]) -> Product:
        pid = product_data.get("id") or str(uuid.uuid4())
        product_data["id"] = pid
        # Auto-compute numericPrice or price if needed
        if "numericPrice" in product_data and ("price" not in product_data or not product_data["price"]):
            np = float(product_data["numericPrice"])
            product_data["price"] = f"₹{int(np):,}" if np >= 500 else f"${np:.2f}"
        elif "price" in product_data and ("numericPrice" not in product_data or product_data["numericPrice"] is None):
            cleaned = "".join([c for c in str(product_data["price"]) if c.isdigit() or c == "."])
            product_data["numericPrice"] = float(cleaned) if cleaned else 0.0

        db = get_firestore_client()
        if db:
            try:
                db.collection("products").document(pid).set(product_data)
            except Exception as e:
                logger.warning(f"Error adding product to Firestore: {e}")

        cls._memory_products[pid] = dict(product_data)
        return Product(**product_data)

    @classmethod
    def update_product(cls, product_id: str, update_data: Dict[str, Any]) -> Optional[Product]:
        """Update an existing catalog product and guarantee price synchronization."""
        canonical_id = PRODUCT_ALIASES.get(product_id, product_id)
        existing = cls.get_product(canonical_id) or cls.get_product(product_id)
        if not existing:
            return None

        current_dict = existing.model_dump()
        for k, v in update_data.items():
            if v is not None and k != "id":
                current_dict[k] = v

        # Currency and Price Synchronization:
        if "numericPrice" in update_data and "price" not in update_data:
            np = float(update_data["numericPrice"])
            is_inr = "₹" in str(existing.price) or np >= 500
            current_dict["price"] = f"₹{int(np):,}" if (is_inr and np.is_integer()) else (f"₹{np:,.2f}" if is_inr else f"${np:.2f}")
            current_dict["numericPrice"] = np
        elif "price" in update_data and "numericPrice" not in update_data:
            cleaned = "".join([c for c in str(update_data["price"]) if c.isdigit() or c == "."])
            current_dict["numericPrice"] = float(cleaned) if cleaned else 0.0
            current_dict["price"] = str(update_data["price"]).strip()
        elif "numericPrice" in update_data and "price" in update_data:
            current_dict["numericPrice"] = float(update_data["numericPrice"])
            current_dict["price"] = str(update_data["price"]).strip()

        target_id = existing.id or canonical_id
        current_dict["id"] = target_id

        db = get_firestore_client()
        if db:
            try:
                db.collection("products").document(target_id).set(current_dict)
            except Exception as e:
                logger.warning(f"Error updating product in Firestore: {e}")

        cls._memory_products[target_id] = dict(current_dict)
        if product_id != target_id:
            cls._memory_products[product_id] = dict(current_dict)
        return Product(**current_dict)

    @classmethod
    def delete_product(cls, product_id: str) -> bool:
        """Delete a product from the catalog."""
        db = get_firestore_client()
        if db:
            try:
                db.collection("products").document(product_id).delete()
            except Exception as e:
                logger.warning(f"Error deleting product from Firestore: {e}")

        if product_id in cls._memory_products:
            del cls._memory_products[product_id]
            return True
        return False

    # =========================================================================
    # CART MANAGEMENT
    # =========================================================================

    @classmethod
    def get_cart(cls, session_id: str) -> Cart:
        data = None
        db = get_firestore_client()
        if db:
            try:
                doc = db.collection("carts").document(session_id).get()
                if doc.exists:
                    data = doc.to_dict()
            except Exception as e:
                logger.warning(f"Error getting cart from Firestore: {e}")

        if not data:
            if session_id not in cls._memory_carts:
                cls._memory_carts[session_id] = {
                    "session_id": session_id,
                    "items": [],
                    "subtotal": 0.0,
                    "subtotal_formatted": "$0.00",
                    "total_items": 0
                }
            data = cls._memory_carts[session_id]

        cart = Cart(**data)
        # Authoritatively synchronize cart items with current product catalog
        updated = False
        refreshed_items = []
        for itm in cart.items:
            prod = cls.get_product(itm.product_id)
            if prod:
                if abs(itm.price - prod.numericPrice) > 0.01 or itm.price_formatted != prod.price:
                    itm.price = prod.numericPrice
                    itm.price_formatted = prod.price
                    updated = True
            refreshed_items.append(itm)

        if updated:
            subtotal = sum(i.price * i.quantity for i in refreshed_items)
            is_inr = any("₹" in (i.price_formatted or "") or i.price >= 500 for i in refreshed_items)
            subtotal_fmt = f"₹{round(subtotal):,}" if is_inr else f"${subtotal:.2f}"
            cart = Cart(
                session_id=session_id,
                items=refreshed_items,
                subtotal=round(subtotal, 2),
                subtotal_formatted=subtotal_fmt,
                total_items=sum(i.quantity for i in refreshed_items)
            )
            if db:
                try:
                    db.collection("carts").document(session_id).set(cart.model_dump())
                except Exception:
                    pass
            cls._memory_carts[session_id] = cart.model_dump()

        return cart

    @classmethod
    def add_to_cart(cls, session_id: str, product_id: str, size: str = "M", quantity: int = 1) -> Cart:
        product = cls.get_product(product_id)
        if not product:
            raise ValueError(f"Product '{product_id}' not found.")

        cart = cls.get_cart(session_id)
        items = list(cart.items)

        found = False
        for item in items:
            if item.product_id == product.id and item.size == size:
                item.quantity += quantity
                item.price = product.numericPrice
                item.price_formatted = product.price
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
        is_inr = any("₹" in (i.price_formatted or "") or i.price >= 500 for i in items)
        subtotal_fmt = f"₹{round(subtotal):,}" if is_inr else f"${subtotal:.2f}"

        updated_cart = Cart(
            session_id=session_id,
            items=items,
            subtotal=round(subtotal, 2),
            subtotal_formatted=subtotal_fmt,
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
        is_inr = any("₹" in (i.price_formatted or "") or i.price >= 500 for i in items)
        subtotal_fmt = f"₹{round(subtotal):,}" if is_inr else f"${subtotal:.2f}"

        updated_cart = Cart(
            session_id=session_id,
            items=items,
            subtotal=round(subtotal, 2),
            subtotal_formatted=subtotal_fmt,
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

    # =========================================================================
    # USER & AUTHENTICATION MANAGEMENT
    # =========================================================================

    @classmethod
    def get_user_by_email(cls, email: str) -> Optional[Dict[str, Any]]:
        clean_email = email.strip().lower()
        db = get_firestore_client()
        if db:
            try:
                doc = db.collection("users").document(clean_email).get()
                if doc.exists:
                    return doc.to_dict()
            except Exception as e:
                logger.warning(f"Firestore get_user_by_email error: {e}")

        return cls._memory_users.get(clean_email)

    @classmethod
    def get_user_by_id(cls, user_id: str) -> Optional[Dict[str, Any]]:
        db = get_firestore_client()
        if db:
            try:
                docs = list(db.collection("users").where("user_id", "==", user_id).limit(1).stream())
                if docs:
                    return docs[0].to_dict()
            except Exception as e:
                logger.warning(f"Firestore get_user_by_id error: {e}")

        for u in cls._memory_users.values():
            if u.get("user_id") == user_id:
                return u
        return None

    @classmethod
    def create_user(cls, user_data: Dict[str, Any]) -> Dict[str, Any]:
        email = user_data["email"].strip().lower()
        user_data["email"] = email
        user_data.setdefault("role", "CUSTOMER")
        user_data.setdefault("addresses", [])
        user_data.setdefault("wishlist", [])
        user_data.setdefault("created_at", datetime.now(timezone.utc).isoformat())

        db = get_firestore_client()
        if db:
            try:
                db.collection("users").document(email).set(user_data)
                logger.info(f"User {email} saved to Firestore (role: {user_data.get('role')}).")
            except Exception as e:
                logger.warning(f"Firestore create_user error: {e}")

        cls._memory_users[email] = dict(user_data)
        return user_data

    @classmethod
    def update_user(cls, email: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        clean_email = email.strip().lower()
        existing = cls.get_user_by_email(clean_email)
        if not existing:
            return None

        for k, v in update_data.items():
            if v is not None and k != "email" and k != "user_id":
                existing[k] = v
        existing["updated_at"] = datetime.now(timezone.utc).isoformat()

        db = get_firestore_client()
        if db:
            try:
                db.collection("users").document(clean_email).set(existing)
            except Exception as e:
                logger.warning(f"Firestore update_user error: {e}")

        cls._memory_users[clean_email] = dict(existing)
        return existing

    @classmethod
    def list_users(cls, limit: int = 100, role: Optional[str] = None) -> List[Dict[str, Any]]:
        db = get_firestore_client()
        users = []
        if db:
            try:
                ref = db.collection("users")
                if role:
                    ref = ref.where("role", "==", role.upper())
                docs = ref.limit(limit).stream()
                for doc in docs:
                    data = doc.to_dict()
                    data.pop("password_hash", None)
                    users.append(data)
                return users
            except Exception as e:
                logger.warning(f"Firestore list_users error: {e}")

        for u in cls._memory_users.values():
            if not role or u.get("role", "").upper() == role.upper():
                copy_u = dict(u)
                copy_u.pop("password_hash", None)
                users.append(copy_u)
        return users[:limit]

    @classmethod
    def count_admins(cls) -> int:
        db = get_firestore_client()
        if db:
            try:
                docs = list(db.collection("users").where("role", "==", "ADMIN").stream())
                return len(docs)
            except Exception as e:
                logger.warning(f"Firestore count_admins error: {e}")

        return sum(1 for u in cls._memory_users.values() if u.get("role") == "ADMIN")

    # Wishlist operations
    @classmethod
    def get_user_wishlist(cls, email: str) -> List[str]:
        user = cls.get_user_by_email(email)
        return user.get("wishlist", []) if user else []

    @classmethod
    def add_to_wishlist(cls, email: str, product_id: str) -> List[str]:
        user = cls.get_user_by_email(email)
        if not user:
            return []
        wl = set(user.get("wishlist", []))
        wl.add(product_id)
        updated_wl = list(wl)
        cls.update_user(email, {"wishlist": updated_wl})
        return updated_wl

    @classmethod
    def remove_from_wishlist(cls, email: str, product_id: str) -> List[str]:
        user = cls.get_user_by_email(email)
        if not user:
            return []
        wl = [pid for pid in user.get("wishlist", []) if pid != product_id]
        cls.update_user(email, {"wishlist": wl})
        return wl

    # Addresses operations
    @classmethod
    def update_user_addresses(cls, email: str, addresses: list) -> List[dict]:
        user = cls.get_user_by_email(email)
        if not user:
            return []
        cls.update_user(email, {"addresses": addresses})
        return addresses

    # =========================================================================
    # ORDERS & CHECKOUT ENGINE
    # =========================================================================

    @classmethod
    def create_order(cls, order_data: Dict[str, Any]) -> Order:
        order_id = order_data.get("id") or f"ORD-{uuid.uuid4().hex[:8].upper()}"
        items_raw = order_data.get("items", [])
        validated_items: List[OrderItem] = []

        # Authoritative Backend Price Calculation & Anti-Manipulation Validation
        for raw in items_raw:
            item_dict = raw if isinstance(raw, dict) else raw.model_dump()
            pid = str(item_dict.get("product_id") or item_dict.get("id") or "")
            prod = cls.get_product(pid)

            if prod is not None:
                authoritative_price = float(prod.numericPrice)
                submitted_price = float(item_dict.get("price", 0.0))

                # If the submitted price deviates from the authoritative database price, reject the order
                if abs(submitted_price - authoritative_price) > 0.01:
                    logger.warning(
                        f"Price tampering detected for product '{pid}' in order '{order_id}'. "
                        f"Submitted: {submitted_price}, Authoritative: {authoritative_price}"
                    )
                    raise ValueError(
                        f"Price manipulation detected for product '{pid}'. "
                        f"Submitted price: {submitted_price:.2f}, Authoritative catalog price: {authoritative_price:.2f}"
                    )

                # Enforce authoritative catalog price
                item_dict["price"] = authoritative_price

            validated_items.append(OrderItem(**item_dict))

        subtotal = round(sum(i.price * i.quantity for i in validated_items), 2)
        delivery_charge = float(order_data.get("delivery_charge", 0.0))
        discount = float(order_data.get("discount", 0.0))
        tax = round((subtotal * 0.18) / 1.18, 2) # GST inclusive
        total = round(subtotal + delivery_charge - discount, 2)

        payment_method = order_data.get("payment_method", "card")
        payment_reference = order_data.get("payment_reference")
        payment_status = order_data.get("payment_status", "PENDING")
        status = order_data.get("status", "CONFIRMED")

        order = Order(
            id=order_id,
            customer_id=order_data.get("customer_id"),
            customer_name=order_data.get("customer_name", "Anonymous Member"),
            customer_email=order_data.get("customer_email", ""),
            customer_phone=order_data.get("customer_phone"),
            shipping_address=order_data.get("shipping_address", "Atelier Member Express Delivery"),
            items=validated_items,
            subtotal=subtotal,
            tax=tax,
            delivery_charge=delivery_charge,
            discount=discount,
            total=total,
            payment_method=payment_method,
            payment_reference=payment_reference,
            payment_status=payment_status,
            status=status,
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat()
        )

        db = get_firestore_client()
        if db:
            try:
                db.collection("orders").document(order_id).set(order.model_dump())
                logger.info(f"Order {order_id} saved to Firestore (status: {status}).")
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
    def get_orders_for_customer(cls, email: str) -> List[Order]:
        clean_email = email.strip().lower()
        db = get_firestore_client()
        orders = []

        if db:
            try:
                docs = db.collection("orders").where("customer_email", "==", clean_email).order_by("created_at", direction="DESCENDING").stream()
                for doc in docs:
                    orders.append(Order(**doc.to_dict()))
                return orders
            except Exception as e:
                logger.warning(f"Firestore get_orders_for_customer error: {e}. Falling back to memory.")

        for o in cls._memory_orders.values():
            if o.get("customer_email", "").strip().lower() == clean_email:
                orders.append(Order(**o))

        orders.sort(key=lambda x: str(x.created_at), reverse=True)
        return orders

    @classmethod
    def list_orders(cls) -> List[Order]:
        """List orders (legacy compatibility)."""
        return cls.list_orders_admin()

    @classmethod
    def list_orders_admin(cls, status: Optional[str] = None, search: Optional[str] = None, limit: int = 100) -> List[Order]:
        db = get_firestore_client()
        orders = []

        if db:
            try:
                ref = db.collection("orders")
                if status:
                    ref = ref.where("status", "==", status.upper())
                docs = ref.order_by("created_at", direction="DESCENDING").limit(limit).stream()
                for doc in docs:
                    orders.append(Order(**doc.to_dict()))
            except Exception as e:
                logger.warning(f"Firestore list_orders_admin error: {e}")
                orders = [Order(**o) for o in cls._memory_orders.values()]
        else:
            orders = [Order(**o) for o in cls._memory_orders.values()]

        # Memory filtering if needed
        results = []
        for o in orders:
            if status and o.status.upper() != status.upper():
                continue
            if search:
                s_lower = search.lower()
                matches_id = s_lower in o.id.lower()
                matches_cust = s_lower in o.customer_name.lower() or s_lower in o.customer_email.lower()
                matches_ref = s_lower in str(o.payment_reference or "").lower()
                if not (matches_id or matches_cust or matches_ref):
                    continue
            results.append(o)

        results.sort(key=lambda x: str(x.created_at), reverse=True)
        return results[:limit]

    @classmethod
    def update_order_status(
        cls,
        order_id: str,
        new_status: str,
        notes: Optional[str] = None,
        tracking_number: Optional[str] = None,
        payment_status: Optional[str] = None,
        updated_by: Optional[str] = None
    ) -> Optional[Order]:
        order = cls.get_order(order_id)
        if not order:
            return None

        order_dict = order.model_dump()
        order_dict["status"] = new_status.upper()
        order_dict["updated_at"] = datetime.now(timezone.utc).isoformat()
        if notes:
            order_dict["admin_notes"] = notes
        if tracking_number:
            order_dict["tracking_number"] = tracking_number
        if payment_status:
            order_dict["payment_status"] = payment_status.upper()

        db = get_firestore_client()
        if db:
            try:
                db.collection("orders").document(order_id).set(order_dict)
            except Exception as e:
                logger.warning(f"Firestore update_order_status error: {e}")

        cls._memory_orders[order_id] = order_dict
        if updated_by:
            cls.log_admin_action(updated_by, f"Updated order {order_id} status to {new_status}")
        return Order(**order_dict)

    @classmethod
    def request_order_cancellation(cls, order_id: str, customer_email: str, reason: str) -> Optional[Order]:
        order = cls.get_order(order_id)
        if not order or order.customer_email.strip().lower() != customer_email.strip().lower():
            return None

        # Eligible if order is not already delivered or cancelled
        if order.status.upper() in ["DELIVERED", "CANCELLED", "REFUNDED"]:
            raise ValueError(f"Order cannot be cancelled in state '{order.status}'.")

        order_dict = order.model_dump()
        order_dict["status"] = "CANCELLED"
        order_dict["cancellation_reason"] = reason
        order_dict["updated_at"] = datetime.now(timezone.utc).isoformat()

        db = get_firestore_client()
        if db:
            try:
                db.collection("orders").document(order_id).set(order_dict)
            except Exception as e:
                logger.warning(f"Firestore cancel order error: {e}")

        cls._memory_orders[order_id] = order_dict
        return Order(**order_dict)

    @classmethod
    def request_order_refund(cls, order_id: str, customer_email: str, reason: str) -> Optional[Order]:
        order = cls.get_order(order_id)
        if not order or order.customer_email.strip().lower() != customer_email.strip().lower():
            return None

        order_dict = order.model_dump()
        order_dict["status"] = "REFUND_REQUESTED"
        order_dict["refund_reason"] = reason
        order_dict["updated_at"] = datetime.now(timezone.utc).isoformat()

        db = get_firestore_client()
        if db:
            try:
                db.collection("orders").document(order_id).set(order_dict)
            except Exception as e:
                logger.warning(f"Firestore refund request error: {e}")

        cls._memory_orders[order_id] = order_dict
        return Order(**order_dict)

    # =========================================================================
    # PAYMENTS & TRANSACTIONS
    # =========================================================================

    @classmethod
    def check_duplicate_utr(cls, utr: str) -> bool:
        """Returns True if the 12-digit UTR has already been submitted in any order or payment."""
        clean_utr = utr.strip()
        # Check memory orders
        for o in cls._memory_orders.values():
            if o.get("payment_reference") == clean_utr or clean_utr in str(o.get("payment_method", "")):
                return True
        # Check memory payments
        for p in cls._memory_payments.values():
            if p.get("utr_reference") == clean_utr:
                return True

        db = get_firestore_client()
        if db:
            try:
                docs = list(db.collection("payments").where("utr_reference", "==", clean_utr).limit(1).stream())
                if docs:
                    return True
                order_docs = list(db.collection("orders").where("payment_reference", "==", clean_utr).limit(1).stream())
                if order_docs:
                    return True
            except Exception as e:
                logger.warning(f"Firestore check_duplicate_utr error: {e}")

        return False

    @classmethod
    def record_payment(cls, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        payment_id = payment_data.get("payment_id") or f"PAY-{uuid.uuid4().hex[:8].upper()}"
        payment_data["payment_id"] = payment_id
        payment_data.setdefault("created_at", datetime.now(timezone.utc).isoformat())
        payment_data.setdefault("status", "UNDER_REVIEW")

        db = get_firestore_client()
        if db:
            try:
                db.collection("payments").document(payment_id).set(payment_data)
            except Exception as e:
                logger.warning(f"Firestore record_payment error: {e}")

        cls._memory_payments[payment_id] = dict(payment_data)
        return payment_data

    @classmethod
    def get_payments(cls, order_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        db = get_firestore_client()
        payments = []
        if db:
            try:
                ref = db.collection("payments")
                if order_id:
                    ref = ref.where("order_id", "==", order_id)
                if status:
                    ref = ref.where("status", "==", status.upper())
                docs = ref.order_by("created_at", direction="DESCENDING").limit(100).stream()
                for doc in docs:
                    payments.append(doc.to_dict())
                return payments
            except Exception as e:
                logger.warning(f"Firestore get_payments error: {e}")

        for p in cls._memory_payments.values():
            if order_id and p.get("order_id") != order_id:
                continue
            if status and p.get("status", "").upper() != status.upper():
                continue
            payments.append(p)
        payments.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)
        return payments

    @classmethod
    def verify_payment(cls, payment_id: str, verified_by: str, status: str = "VERIFIED") -> Optional[Dict[str, Any]]:
        db = get_firestore_client()
        payment = None
        if db:
            try:
                doc = db.collection("payments").document(payment_id).get()
                if doc.exists:
                    payment = doc.to_dict()
            except Exception as e:
                logger.warning(f"Firestore verify_payment get error: {e}")

        if not payment:
            payment = cls._memory_payments.get(payment_id)

        if not payment:
            return None

        payment["status"] = status.upper()
        payment["verified_by"] = verified_by
        payment["verified_at"] = datetime.now(timezone.utc).isoformat()

        if db:
            try:
                db.collection("payments").document(payment_id).set(payment)
            except Exception as e:
                logger.warning(f"Firestore verify_payment set error: {e}")

        cls._memory_payments[payment_id] = payment

        # Also update linked order if verified
        order_id = payment.get("order_id")
        if order_id:
            new_order_status = "CONFIRMED" if status.upper() == "VERIFIED" else "PAYMENT_FAILED"
            cls.update_order_status(
                order_id=order_id,
                new_status=new_order_status,
                payment_status=status.upper(),
                updated_by=verified_by,
                notes=f"Payment {payment_id} marked {status} by admin."
            )

        cls.log_admin_action(verified_by, f"Marked payment {payment_id} as {status}")
        return payment

    # =========================================================================
    # ADMIN ANALYTICS & ACTIVITY LOGS
    # =========================================================================

    @classmethod
    def get_admin_dashboard_metrics(cls) -> Dict[str, Any]:
        """Calculates real-time business statistics from orders, products, and users."""
        orders = cls.list_orders_admin(limit=500)
        products = cls.get_all_products()
        users = cls.list_users(limit=500, role="CUSTOMER")

        total_orders = len(orders)
        total_revenue = sum(float(o.total) for o in orders if o.status.upper() not in ["CANCELLED", "PAYMENT_FAILED"])
        total_customers = len(users)

        pending_orders = sum(1 for o in orders if o.status.upper() in ["PAYMENT_PENDING", "PAYMENT_UNDER_REVIEW", "PENDING"])
        successful_payments = sum(1 for o in orders if o.payment_status.upper() == "VERIFIED" or o.status.upper() in ["CONFIRMED", "PROCESSING", "PACKED", "SHIPPED", "DELIVERED"])
        failed_payments = sum(1 for o in orders if o.payment_status.upper() == "FAILED" or o.status.upper() == "PAYMENT_FAILED")
        refund_requests = sum(1 for o in orders if o.status.upper() in ["REFUND_REQUESTED", "REFUNDED"])
        low_stock_products = sum(1 for p in products if not p.in_stock)

        return {
            "total_revenue_usd": round(total_revenue, 2),
            "total_revenue_inr": round(total_revenue * 86.50, 2),
            "total_orders": total_orders,
            "total_customers": total_customers,
            "pending_orders": pending_orders,
            "successful_payments": successful_payments,
            "failed_payments": failed_payments,
            "refund_requests": refund_requests,
            "low_stock_products": low_stock_products
        }

    @classmethod
    def log_admin_action(cls, admin_email: str, action: str, details: Optional[Dict[str, Any]] = None):
        log_entry = {
            "log_id": f"LOG-{uuid.uuid4().hex[:8].upper()}",
            "admin_email": admin_email,
            "action": action,
            "details": details or {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        db = get_firestore_client()
        if db:
            try:
                db.collection("admin_activity_logs").document(log_entry["log_id"]).set(log_entry)
            except Exception as e:
                logger.warning(f"Firestore log_admin_action error: {e}")

        cls._memory_admin_logs.insert(0, log_entry)

    @classmethod
    def get_admin_logs(cls, limit: int = 50) -> List[Dict[str, Any]]:
        db = get_firestore_client()
        logs = []
        if db:
            try:
                docs = db.collection("admin_activity_logs").order_by("timestamp", direction="DESCENDING").limit(limit).stream()
                for doc in docs:
                    logs.append(doc.to_dict())
                return logs
            except Exception as e:
                logger.warning(f"Firestore get_admin_logs error: {e}")

        return cls._memory_admin_logs[:limit]
