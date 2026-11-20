import json
import sys
from fastapi.testclient import TestClient
from backend.main import app
from backend.services.firestore_service import FirestoreService
from backend.config import ADMIN_EMAIL, ADMIN_INITIAL_PASSWORD

def run_tests():
    print("=" * 70)
    print("STARTING COMPLETE E2E PRICE SYNCHRONIZATION TEST SUITE")
    print("=" * 70)

    client = TestClient(app)

    # -------------------------------------------------------------
    # STEP 1: Select an existing shoe product
    # -------------------------------------------------------------
    print("\n--- STEP 1: Select an existing shoe product ---")
    shoe_id = "luka-5"
    # Ensure it's in Firestore with original test baseline
    FirestoreService.update_product(shoe_id, {
        "title": "LUKA 5",
        "name": "LUKA 5",
        "category": "sneakers",
        "numericPrice": 4999.0,
        "price": "₹4,999"
    })
    shoe = FirestoreService.get_product(shoe_id)
    assert shoe is not None, f"Product {shoe_id} must exist"
    print(f"Selected product: ID={shoe.id}, Title='{shoe.title}', Category='{shoe.category}'")

    # -------------------------------------------------------------
    # STEP 2: Record its original price
    # -------------------------------------------------------------
    print("\n--- STEP 2: Record its original price ---")
    original_numeric = shoe.numericPrice
    original_formatted = shoe.price
    print(f"Original Price Recorded: numericPrice={original_numeric}, formatted='{original_formatted}'")
    assert original_numeric == 4999.0, f"Expected 4999.0, got {original_numeric}"
    assert original_formatted == "₹4,999", f"Expected ₹4,999, got {original_formatted}"

    # -------------------------------------------------------------
    # STEP 3: Log in as admin
    # -------------------------------------------------------------
    print("\n--- STEP 3: Log in as admin ---")
    login_resp = client.post("/api/auth/admin-login", json={
        "email": ADMIN_EMAIL,
        "password": ADMIN_INITIAL_PASSWORD
    })
    print(f"Admin login status: {login_resp.status_code}")
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    token_data = login_resp.json()
    admin_token = token_data.get("token") or token_data.get("access_token")
    assert admin_token, "Admin token must be returned"
    headers = {"Authorization": f"Bearer {admin_token}"}
    print("Admin successfully authenticated. Token acquired.")

    # -------------------------------------------------------------
    # STEP 4 & 5: Change price from ₹4,999 to ₹3,999 and Save Changes
    # -------------------------------------------------------------
    print("\n--- STEP 4 & 5: Change price from ₹4,999 to ₹3,999 & Save changes ---")
    new_price_num = 3999.0
    new_price_fmt = "₹3,999"
    update_payload = {
        "title": "LUKA 5",
        "numericPrice": new_price_num,
        "price": new_price_fmt,
        "desc": "Engineered for rapid step-backs and directional shifts with IsoPlate stability."
    }

    # Test Admin PUT endpoint
    put_resp = client.put(f"/api/admin/products/{shoe_id}", json=update_payload, headers=headers)
    print(f"PUT /api/admin/products/{shoe_id} status: {put_resp.status_code}")
    assert put_resp.status_code == 200, f"Update failed: {put_resp.text}"
    updated_data = put_resp.json()
    print(f"Response from backend after save: numericPrice={updated_data.get('numericPrice')}, price='{updated_data.get('price')}'")
    assert updated_data.get("numericPrice") == new_price_num
    assert updated_data.get("price") == new_price_fmt

    # -------------------------------------------------------------
    # STEP 6: Verify the updated Firestore document
    # -------------------------------------------------------------
    print("\n--- STEP 6: Verify the updated Firestore document ---")
    db_product = FirestoreService.get_product(shoe_id)
    assert db_product is not None
    print(f"Firestore Document State: ID={db_product.id}, numericPrice={db_product.numericPrice}, price='{db_product.price}'")
    assert db_product.numericPrice == 3999.0, f"Firestore numericPrice expected 3999.0, got {db_product.numericPrice}"
    assert db_product.price == "₹3,999", f"Firestore price expected ₹3,999, got {db_product.price}"
    print("VERIFIED: Firestore document has been updated and persisted correctly.")

    # -------------------------------------------------------------
    # STEP 7: Open the customer storefront
    # -------------------------------------------------------------
    print("\n--- STEP 7: Open the customer storefront (GET /api/products) ---")
    store_resp = client.get("/api/products")
    assert store_resp.status_code == 200
    # Verify Cache-Control headers
    cc_header = store_resp.headers.get("Cache-Control", "")
    print(f"Storefront API Cache-Control Header: '{cc_header}'")
    assert "no-cache" in cc_header and "no-store" in cc_header, "Storefront must return no-cache, no-store headers"

    products = store_resp.json()
    store_shoe = next((p for p in products if p["id"] == shoe_id), None)
    assert store_shoe is not None, f"Shoe {shoe_id} not found in storefront products"

    # -------------------------------------------------------------
    # STEP 8: Verify the same shoe displays ₹3,999
    # -------------------------------------------------------------
    print("\n--- STEP 8: Verify the same shoe displays ₹3,999 ---")
    print(f"Storefront product data: ID={store_shoe['id']}, price='{store_shoe['price']}', numericPrice={store_shoe['numericPrice']}")
    assert store_shoe["numericPrice"] == 3999.0, f"Expected 3999.0, got {store_shoe['numericPrice']}"
    assert store_shoe["price"] == "₹3,999", f"Expected ₹3,999, got {store_shoe['price']}"
    print("VERIFIED: Customer storefront receives ₹3,999.")

    # -------------------------------------------------------------
    # STEP 9: Refresh the browser and verify it still displays ₹3,999
    # -------------------------------------------------------------
    print("\n--- STEP 9: Refresh browser (simulated cache-busting fetch) ---")
    refresh_resp = client.get(f"/api/products?_t=1700000000000")
    assert refresh_resp.status_code == 200
    refreshed_prods = refresh_resp.json()
    refreshed_shoe = next((p for p in refreshed_prods if p["id"] == shoe_id), None)
    assert refreshed_shoe is not None
    assert refreshed_shoe["numericPrice"] == 3999.0
    assert refreshed_shoe["price"] == "₹3,999"
    print("VERIFIED: Refreshed browser still displays ₹3,999 consistently.")

    # -------------------------------------------------------------
    # STEP 10: Add the shoe to the shopping bag
    # -------------------------------------------------------------
    print("\n--- STEP 10: Add the shoe to the shopping bag ---")
    session_id = "test-session-cart-sync"
    cart_resp = client.post(f"/api/cart/{session_id}/items", json={
        "product_id": shoe_id,
        "size": "42",
        "quantity": 1
    })
    print(f"Add to cart status: {cart_resp.status_code}")
    assert cart_resp.status_code == 200
    cart_data = cart_resp.json()
    print(f"Cart State: Subtotal={cart_data['subtotal']}, SubtotalFormatted='{cart_data['subtotal_formatted']}', Items={len(cart_data['items'])}")
    assert cart_data["subtotal"] == 3999.0
    assert cart_data["items"][0]["price"] == 3999.0
    print("VERIFIED: Shopping bag accurately holds shoe at authoritative ₹3,999.")

    # -------------------------------------------------------------
    # STEP 11: Verify checkout uses ₹3,999
    # -------------------------------------------------------------
    print("\n--- STEP 11: Verify checkout uses ₹3,999 ---")
    order_payload = {
        "customer_name": "Test Patron",
        "customer_email": "patron@atelier.luxury",
        "shipping_address": "Atelier Luxury Suite, Delhi",
        "payment_method": "card",
        "items": [
            {
                "product_id": shoe_id,
                "title": "LUKA 5",
                "size": "42",
                "quantity": 1,
                "price": 3999.0
            }
        ]
    }
    order_resp = client.post("/api/orders", json=order_payload)
    print(f"Checkout / Place Order status: {order_resp.status_code}")
    assert order_resp.status_code == 201, f"Checkout failed: {order_resp.text}"
    placed_order = order_resp.json()
    print(f"Placed Order: ID={placed_order['id']}, Subtotal={placed_order['subtotal']}, Total={placed_order['total']}")
    assert placed_order["subtotal"] == 3999.0
    assert placed_order["total"] == 3999.0
    print("VERIFIED: Checkout successfully processed order using ₹3,999.")

    # -------------------------------------------------------------
    # STEP 12: Verify backend rejects manipulated frontend prices
    # -------------------------------------------------------------
    print("\n--- STEP 12: Verify backend rejects manipulated frontend prices ---")
    # A malicious client attempts to change the price from ₹3,999 to ₹1.00 or ₹100.00
    tampered_payload = {
        "customer_name": "Tamper Attempt",
        "customer_email": "tamper@atelier.luxury",
        "shipping_address": "Nowhere",
        "payment_method": "card",
        "items": [
            {
                "product_id": shoe_id,
                "title": "LUKA 5",
                "size": "42",
                "quantity": 1,
                "price": 1.00 # Tampered price!
            }
        ]
    }
    tampered_resp = client.post("/api/orders", json=tampered_payload)
    print(f"Tampered order submission HTTP Status: {tampered_resp.status_code}")
    print(f"Tampered order error detail: {tampered_resp.json().get('detail')}")
    assert tampered_resp.status_code == 400, "Backend must reject manipulated prices with HTTP 400"
    assert "manipulation" in tampered_resp.json().get("detail", "").lower() or "tampering" in tampered_resp.json().get("detail", "").lower()
    print("VERIFIED: Backend rejects manipulated frontend prices immediately.")

    # Test UPI gateway anti-tampering as well
    upi_tampered = client.post("/api/upi/create-intent", json={
        "orderId": "ORD-TAMPER",
        "amountUsd": 10.0, # Tampered amount!
        "customerName": "Tamper",
        "customerEmail": "tamper@atelier.luxury",
        "items": [
            {
                "product_id": shoe_id,
                "title": "LUKA 5",
                "size": "42",
                "quantity": 1,
                "price": 10.0
            }
        ]
    })
    print(f"UPI intent tampered price status: {upi_tampered.status_code}")
    assert upi_tampered.status_code == 400
    print("VERIFIED: UPI intent also strictly rejects manipulated prices.")

    # -------------------------------------------------------------
    # TEST 13: Test with newly created product
    # -------------------------------------------------------------
    print("\n--- TEST 13: Test with newly created product ---")
    new_prod_id = "test-edition-sneaker"
    new_prod_payload = {
        "id": new_prod_id,
        "title": "TEST RUNWAY SNEAKER",
        "name": "TEST RUNWAY SNEAKER",
        "subtitle": "Limited Concept Sneaker",
        "category": "sneakers",
        "numericPrice": 7500.0,
        "price": "₹7,500",
        "in_stock": True,
        "sizes": ["41", "42", "43"],
        "desc": "Limited test sneaker created via Admin API"
    }
    # Create product via Admin API
    create_resp = client.post("/api/admin/products", json=new_prod_payload, headers=headers)
    print(f"Create new product status: {create_resp.status_code}")
    assert create_resp.status_code == 201

    # Verify newly created product in Firestore
    created_shoe = FirestoreService.get_product(new_prod_id)
    assert created_shoe is not None
    assert created_shoe.numericPrice == 7500.0
    assert created_shoe.price == "₹7,500"
    print(f"Created Product Verified in Firestore: ID={created_shoe.id}, Price={created_shoe.price}")

    # Verify newly created product in Storefront
    store_new_resp = client.get(f"/api/products/{new_prod_id}")
    assert store_new_resp.status_code == 200
    assert store_new_resp.json()["numericPrice"] == 7500.0
    assert store_new_resp.json()["price"] == "₹7,500"
    print(f"Created Product Verified in Storefront: ID={new_prod_id}, Price={store_new_resp.json()['price']}")

    # Update newly created product price from ₹7,500 to ₹6,200
    update_new_resp = client.put(f"/api/admin/products/{new_prod_id}", json={
        "numericPrice": 6200.0,
        "price": "₹6,200"
    }, headers=headers)
    assert update_new_resp.status_code == 200
    assert update_new_resp.json()["numericPrice"] == 6200.0

    # Storefront reflects updated price for newly created product
    store_new_updated = client.get(f"/api/products/{new_prod_id}")
    assert store_new_updated.json()["numericPrice"] == 6200.0
    assert store_new_updated.json()["price"] == "₹6,200"
    print(f"Newly Created Product Price Update Verified: Now {store_new_updated.json()['price']}")

    # Cleanup test product
    client.delete(f"/api/admin/products/{new_prod_id}", headers=headers)
    print(f"Cleaned up temporary test product {new_prod_id}.")

    print("\n" + "=" * 70)
    print("ALL 13 TESTS PASSED PERFECTLY WITH ZERO REGRESSIONS!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
