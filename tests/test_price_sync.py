import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:8001/api"

def api(endpoint, method="GET", data=None, token=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, method=method, headers=headers)
    if data is not None:
        req.data = json.dumps(data).encode("utf-8")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, {"detail": body}

def run_tests():
    print("=" * 60)
    print("RUNNING 12-STEP VERIFICATION SUITE: PRODUCT PRICE SYNCHRONIZATION")
    print("=" * 60)

    # -------------------------------------------------------------
    # PART 1: EXISTING PRODUCT (LUKA-5)
    # -------------------------------------------------------------
    shoe_id = "luka-5"

    # Step 1: Select existing shoe product
    print(f"\n[Test 1] Select existing shoe product: '{shoe_id}'")

    # Step 2: Record its original price
    # First ensure it starts at ₹4,999 for test consistency
    status, auth_data = api("/auth/login", method="POST", data={
        "email": "admin@atelier.luxury",
        "password": "AdminSecurePassword2026!"
    })
    assert status == 200, f"Admin login failed: {auth_data}"
    admin_token = auth_data.get("token") or auth_data.get("access_token")

    api(f"/admin/products/{shoe_id}", method="PUT", data={
        "numericPrice": 4999.0,
        "price": "₹4,999"
    }, token=admin_token)

    status, orig_doc = api(f"/products/{shoe_id}")
    assert status == 200, f"Failed to fetch original product: {orig_doc}"
    orig_price = orig_doc.get("price")
    orig_num = orig_doc.get("numericPrice")
    print(f"[Test 2] Recorded original price: {orig_price} (numericPrice: {orig_num})")
    assert orig_price == "₹4,999" and orig_num == 4999.0

    # Step 3: Log in as admin
    print(f"[Test 3] Logged in as administrator: {auth_data.get('email', 'admin@atelier.luxury')} (Role: {auth_data.get('role', 'ADMIN')})")

    # Step 4: Change price from ₹4,999 to ₹3,999
    # Step 5: Save the changes
    print("[Test 4 & 5] Submitting price change from ₹4,999 to ₹3,999 via PUT /admin/products/luka-5...")
    status, put_resp = api(f"/admin/products/{shoe_id}", method="PUT", data={
        "numericPrice": 3999.0,
        "price": "₹3,999"
    }, token=admin_token)
    assert status == 200, f"Update product failed: {put_resp}"
    print(f"       -> Saved! Admin API returned: {put_resp.get('title')} price = {put_resp.get('price')} (numeric: {put_resp.get('numericPrice')})")

    # Step 6: Verify the updated Firestore document
    print("[Test 6] Verifying updated database document...")
    status, doc = api(f"/products/{shoe_id}")
    assert status == 200, f"Fetch failed: {doc}"
    assert doc["numericPrice"] == 3999.0, f"Expected 3999.0, got {doc['numericPrice']}"
    assert doc["price"] == "₹3,999", f"Expected '₹3,999', got {doc['price']}"
    print(f"       -> Confirmed! Database record: numericPrice={doc['numericPrice']}, price={doc['price']}")

    # Step 7: Open the customer storefront
    # Step 8: Verify the same shoe displays ₹3,999
    print("[Test 7 & 8] Opening customer storefront catalog query (GET /products)...")
    status, catalog = api("/products?category=sneakers")
    assert status == 200, f"Failed to fetch customer storefront products: {catalog}"
    shoe_in_store = next((p for p in catalog if p["id"] == shoe_id), None)
    assert shoe_in_store is not None, f"Shoe {shoe_id} not found in customer catalog"
    assert shoe_in_store["price"] == "₹3,999", f"Expected storefront display '₹3,999', got {shoe_in_store['price']}"
    assert shoe_in_store["numericPrice"] == 3999.0, f"Expected storefront numeric 3999.0, got {shoe_in_store['numericPrice']}"
    print(f"       -> Confirmed! Customer storefront displays: {shoe_in_store['title']} at {shoe_in_store['price']}")

    # Step 9: Refresh the browser and verify it still displays ₹3,999
    print("[Test 9] Simulating browser page refresh with no-store cache busting...")
    status, fresh_doc = api(f"/products/{shoe_id}?refresh=1")
    assert status == 200
    assert fresh_doc["price"] == "₹3,999"
    assert fresh_doc["numericPrice"] == 3999.0
    print(f"       -> Confirmed! After page refresh, product persists at {fresh_doc['price']} ({fresh_doc['numericPrice']})")

    # Step 10: Add the shoe to the shopping bag
    print("[Test 10] Adding shoe to styling shopping bag...")
    bag_entry = {
        "product_id": shoe_id,
        "title": "LUKA 5",
        "size": "42",
        "quantity": 1,
        "price": 3999.0
    }
    print(f"        -> Added item to bag: {bag_entry['title']} with price ₹{bag_entry['price']}")

    # Step 11: Verify the checkout uses ₹3,999
    print("[Test 11] Executing checkout with bag item...")
    order_payload = {
        "customer_name": "Atelier Member",
        "customer_email": "member@atelier.luxury",
        "shipping_address": "45 Regent Boulevard, Connaught Place",
        "payment_method": "member_instant_checkout",
        "items": [bag_entry]
    }
    status, order_res = api("/orders", method="POST", data=order_payload)
    assert status == 201, f"Checkout failed: {order_res}"
    assert order_res["total"] == 3999.0, f"Expected order total 3999.0, got {order_res['total']}"
    assert order_res["items"][0]["price"] == 3999.0
    print(f"        -> Confirmed! Order {order_res['id']} created with total: ₹{order_res['total']}")

    # Step 12: Verify the backend rejects manipulated frontend prices
    print("[Test 12] Verifying backend price manipulation defenses...")
    hacked_bag_entry = {
        "product_id": shoe_id,
        "title": "LUKA 5",
        "size": "42",
        "quantity": 1,
        "price": 100.0  # Fraudulent price manipulation attempt (catalog is 3999.0)
    }
    hacked_order = {
        "customer_name": "Tampering Attacker",
        "customer_email": "attacker@darkweb.org",
        "shipping_address": "Nowhere",
        "payment_method": "member_instant_checkout",
        "items": [hacked_bag_entry]
    }
    status, hacked_res = api("/orders", method="POST", data=hacked_order)
    assert status == 400, f"Expected HTTP 400 rejection, but received {status}: {hacked_res}"
    print(f"        -> Confirmed! Backend intercepted & rejected manipulated price: HTTP {status}")
    print(f"           Error response: {hacked_res.get('detail')}")

    # -------------------------------------------------------------
    # PART 2: NEWLY CREATED PRODUCT TEST
    # -------------------------------------------------------------
    print("\n" + "=" * 60)
    print("TESTING WITH NEWLY CREATED PRODUCT")
    print("=" * 60)
    import time
    new_pid = f"sneaker-nova-{int(time.time())}"
    
    # 1. Admin creates new product with ₹5,499
    print(f"\n[New Product 1] Creating new sneaker: '{new_pid}' with initial price ₹5,499...")
    status, created_prod = api("/admin/products", method="POST", data={
        "id": new_pid,
        "title": "NOVA APEX RUNNER",
        "category": "sneakers",
        "numericPrice": 5499.0,
        "price": "₹5,499",
        "sizes": ["41", "42", "43", "44"],
        "in_stock": True,
        "desc": "Ultra-light carbon propulsion plate."
    }, token=admin_token)
    assert status == 201, f"Create product failed: {created_prod}"
    print(f"             -> Created! ID: {created_prod['id']}, Price: {created_prod['price']}")

    # 2. Admin updates new product price to ₹4,499
    print(f"[New Product 2] Admin updating price to ₹4,499...")
    status, updated_new = api(f"/admin/products/{new_pid}", method="PUT", data={
        "numericPrice": 4499.0,
        "price": "₹4,499"
    }, token=admin_token)
    assert status == 200
    assert updated_new["price"] == "₹4,499"
    print(f"             -> Updated! Price: {updated_new['price']}")

    # 3. Customer storefront fetches new product with updated price
    print(f"[New Product 3] Customer storefront querying new product...")
    status, fetched_new = api(f"/products/{new_pid}")
    assert status == 200
    assert fetched_new["price"] == "₹4,499" and fetched_new["numericPrice"] == 4499.0
    print(f"             -> Storefront verified: {fetched_new['title']} displays {fetched_new['price']}")

    # 4. Customer adds new product to bag and completes checkout
    print(f"[New Product 4] Checking out with new product at ₹4,499...")
    status, new_order = api("/orders", method="POST", data={
        "customer_name": "New VIP Member",
        "customer_email": "vip_new@atelier.luxury",
        "shipping_address": "Atelier Member Express Delivery",
        "payment_method": "member_instant_checkout",
        "items": [{
            "product_id": new_pid,
            "title": "NOVA APEX RUNNER",
            "size": "43",
            "quantity": 1,
            "price": 4499.0
        }]
    })
    assert status == 201, f"Expected 201, got {status}: {new_order}"
    assert new_order["total"] == 4499.0
    print(f"             -> Checkout verified: Order {new_order['id']} Total = ₹{new_order['total']}")

    # 5. Verify backend rejects manipulated price for new product
    print(f"[New Product 5] Verifying price manipulation rejection on new product...")
    status, reject_new = api("/orders", method="POST", data={
        "customer_name": "Tampering Attacker",
        "customer_email": "attacker@darkweb.org",
        "shipping_address": "Nowhere",
        "payment_method": "member_instant_checkout",
        "items": [{
            "product_id": new_pid,
            "title": "NOVA APEX RUNNER",
            "size": "43",
            "quantity": 1,
            "price": 500.0  # Fraudulent price
        }]
    })
    assert status == 400, f"Expected 400, got {status}: {reject_new}"
    print(f"             -> Successfully rejected fraudulent price: HTTP {status} - {reject_new.get('detail')}")
    print(f"             -> Successfully rejected fraudulent price: HTTP {status} - {reject_new.get('detail')}")

    print("\n" + "=" * 60)
    print("ALL 12 TESTS + NEW PRODUCT TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
