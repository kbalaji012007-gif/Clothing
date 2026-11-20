import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("clothing_agency_backend")

PORT = int(os.getenv("PORT", "8001"))
HOST = os.getenv("HOST", "0.0.0.0")
CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin.strip()]

# Security & JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "atelier_couture_luxury_jwt_secret_key_2026_super_secure_enterprise_grade_auth")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "10080")) # 7 days
ADMIN_BOOTSTRAP_KEY = os.getenv("ADMIN_BOOTSTRAP_KEY", "atelier-bootstrap-2026")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@atelier.luxury")
ADMIN_INITIAL_PASSWORD = os.getenv("ADMIN_INITIAL_PASSWORD", "Admin@Atelier2026")

# Clean import from the decoupled database layer
from database.connection import get_firestore_client, is_firebase_connected, init_firebase

__all__ = [
    "PORT", "HOST", "CORS_ORIGINS", "logger",
    "JWT_SECRET", "JWT_ALGORITHM", "JWT_EXPIRATION_MINUTES",
    "ADMIN_BOOTSTRAP_KEY", "ADMIN_EMAIL", "ADMIN_INITIAL_PASSWORD",
    "get_firestore_client", "is_firebase_connected", "init_firebase"
]
