# Clothing Agency E-Commerce API Backend

Python **FastAPI** backend integrated with **Firebase Cloud Firestore** for product inventory, user shopping bags/carts, and checkout orders.

---

## 🚀 Quick Start

### 1. Requirements & Dependencies
Make sure you have Python 3.11+ installed:
```bash
pip install -r backend/requirements.txt
```

### 2. Run the Backend Server
Run on port **8001** (or configure `PORT` in `.env`):
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001 --reload
```

Interactive Swagger documentation is available at:
👉 **[http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)**

---

## 🔥 Firebase Firestore Integration

The backend supports three seamless modes for connecting to Firebase:

1. **Local Key File (Recommended for Local Dev):**
   - Download your Firebase Service Account JSON key from the Firebase Console (*Project Settings -> Service Accounts -> Generate new private key*).
   - Place it as `backend/serviceAccountKey.json`.
2. **Environment Variable (Recommended for Cloud / Render / Railway):**
   - Set `FIREBASE_CREDENTIALS_JSON` to the raw JSON string of your service account.
3. **Application Default Credentials (GCP SDK):**
   - Automatically detected if `gcloud auth application-default login` has been run.
4. **Development In-Memory Fallback:**
   - If no Firebase credentials are configured yet, the backend automatically runs in in-memory mode with all store products loaded, so development and testing never crash.

---

## 📡 API Endpoints

### Health & Seed
- `GET /api/health` — Service status, Firebase connection state, and catalog stats.
- `POST /api/seed` — Seed or re-sync catalog products into Firestore.

### Products
- `GET /api/products` — List all products (supports `?category=sneakers`, `?category=rack`, `?category=runway`, and `?search=`).
- `GET /api/products/{id}` — Retrieve single product details.
- `POST /api/products` — Create a new product.

### Cart / Shopping Bag
- `GET /api/cart/{session_id}` — Retrieve the user's active bag.
- `POST /api/cart/{session_id}/items` — Add product to bag (`product_id`, `size`, `quantity`).
- `DELETE /api/cart/{session_id}/items/{item_id}` — Remove item from bag.
- `DELETE /api/cart/{session_id}` — Clear bag.

### Orders & Checkout
- `POST /api/orders` — Submit a checkout order directly into the Firestore `orders` collection.
- `GET /api/orders/{id}` — Get order status.
- `GET /api/orders` — List recent orders.
