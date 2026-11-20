import os
import json
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("clothing_agency_database")

_firestore_client = None
_firebase_initialized = False

def init_firebase():
    """Initialize Firebase Admin SDK and return Firestore client."""
    global _firestore_client, _firebase_initialized
    if _firebase_initialized:
        return _firestore_client

    import firebase_admin
    from firebase_admin import credentials, firestore

    # 1. Environment variable JSON string (for Render / Railway / Cloud)
    cred_json_str = os.getenv("FIREBASE_CREDENTIALS_JSON") or os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    if cred_json_str:
        try:
            cred_dict = json.loads(cred_json_str)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            _firestore_client = firestore.client()
            _firebase_initialized = True
            logger.info("Database: Initialized Firebase from FIREBASE_CREDENTIALS_JSON.")
            return _firestore_client
        except Exception as e:
            logger.warning(f"Database: FIREBASE_CREDENTIALS_JSON error: {e}")

    # 2. Local serviceAccountKey.json
    key_path = os.getenv("SERVICE_ACCOUNT_KEY_PATH", "backend/serviceAccountKey.json")
    if not os.path.isabs(key_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        key_path = os.path.join(base_dir, key_path)

    if os.path.exists(key_path):
        try:
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
            _firestore_client = firestore.client()
            _firebase_initialized = True
            logger.info(f"Database: Initialized Firebase from {key_path}.")
            return _firestore_client
        except Exception as e:
            logger.warning(f"Database: File key error ({key_path}): {e}")

    # 3. Application Default Credentials (GCP)
    try:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
        _firestore_client = firestore.client()
        _firebase_initialized = True
        logger.info("Database: Initialized Firebase from Application Default Credentials.")
        return _firestore_client
    except Exception:
        pass

    # 4. Fallback in-memory mode
    logger.info("Database: Running in Development Mock Mode (Credentials not provided).")
    _firebase_initialized = True
    _firestore_client = None
    return None

def get_firestore_client():
    global _firestore_client, _firebase_initialized
    if not _firebase_initialized:
        init_firebase()
    return _firestore_client

def is_firebase_connected() -> bool:
    return get_firestore_client() is not None
