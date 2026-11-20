"""
Standalone Database Seeder for Cloud Firestore.
Run with:
    python -m database.seed
"""
import sys
from .connection import get_firestore_client, is_firebase_connected, logger
from .seed_data import INITIAL_SEED_PRODUCTS

def seed_database(force: bool = False):
    print("Connecting to Firestore...")
    db = get_firestore_client()
    
    if not db:
        print("[Notice] Firebase credentials not configured. Skipping live Firestore seeding.")
        print("To seed live Firestore, place 'backend/serviceAccountKey.json' or set FIREBASE_CREDENTIALS_JSON.")
        return False

    products_ref = db.collection("products")
    existing_docs = list(products_ref.limit(1).stream())
    
    if existing_docs and not force:
        print(f"[OK] Products collection already contains documents. Pass force=True to overwrite.")
        return True

    print(f"Seeding {len(INITIAL_SEED_PRODUCTS)} items into Firestore 'products' collection...")
    batch = db.batch()
    for prod in INITIAL_SEED_PRODUCTS:
        doc_ref = products_ref.document(prod["id"])
        batch.set(doc_ref, prod)
    
    batch.commit()
    print(f"[Success] Seeded {len(INITIAL_SEED_PRODUCTS)} products into Cloud Firestore.")
    return True

if __name__ == "__main__":
    force_flag = "--force" in sys.argv
    seed_database(force=force_flag)
