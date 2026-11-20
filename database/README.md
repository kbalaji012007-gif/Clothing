# Clothing Agency — Database Layer (Firebase Cloud Firestore)

This folder contains the database schema definitions, Firebase connection factory, security rules, and seed scripts.

---

## 📂 Files in `database/`

- **`connection.py`** — Singleton connection provider for the Firebase Admin SDK (`get_firestore_client()`).
- **`seed_data.py`** — Initial product catalog data (all sneakers, clothing rack garments, and runway lookbook pieces).
- **`seed.py`** — Standalone seeder CLI to populate or reset Firestore (`python -m database.seed`).
- **`schema.json`** — Strict JSON schemas for all collections (`products`, `carts`, `orders`, `users`).
- **`firestore.rules`** — Cloud Firestore security rules.

---

## 🗄️ Firestore Collections

1. **`products`**:
   - Stores all catalog items (Sneakers, Clothing Rack apparel, Runway outfits).
2. **`carts`**:
   - Stores session-based carts, line items, chosen sizes, and calculated subtotals.
3. **`orders`**:
   - Records checkout orders with customer names, items, quantities, and totals.
4. **`users`**:
   - Member authentication records, saved sizing preferences, and profile metadata.

---

## ⚡ How to Seed the Database

Run from project root:
```bash
python -m database.seed
```
To force overwrite existing items:
```bash
python -m database.seed --force
```
