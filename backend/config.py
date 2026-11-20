import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("clothing_agency_backend")

PORT = int(os.getenv("PORT", "8001"))
HOST = os.getenv("HOST", "0.0.0.0")
CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin.strip()]

# Clean import from the decoupled database layer
from database.connection import get_firestore_client, is_firebase_connected, init_firebase

__all__ = ["PORT", "HOST", "CORS_ORIGINS", "logger", "get_firestore_client", "is_firebase_connected", "init_firebase"]
