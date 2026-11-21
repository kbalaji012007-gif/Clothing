import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from ..config import logger, ADMIN_BOOTSTRAP_KEY, ADMIN_EMAIL, ADMIN_INITIAL_PASSWORD
from ..services.firestore_service import FirestoreService
from ..security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    require_customer,
    require_admin
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

# =============================================================================
# REQUEST & RESPONSE SCHEMAS
# =============================================================================

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: Optional[str] = None

class BootstrapAdminRequest(BaseModel):
    name: str = "Chief Administrator"
    email: str = "admin@atelier.luxury"
    password: str
    bootstrap_key: Optional[str] = None

class GoogleAuthRequest(BaseModel):
    credential: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None

class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    addresses: Optional[List[Dict[str, Any]]] = None

class AuthResponse(BaseModel):
    token: str
    user_id: str
    name: str
    email: str
    role: str
    message: str

# =============================================================================
# AUTHENTICATION ENDPOINTS
# =============================================================================

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest):
    """
    Register a new customer account with Argon2id password hashing
    and return a signed JWT access token.
    """
    email_clean = payload.email.strip().lower()
    if not email_clean or "@" not in email_clean:
        raise HTTPException(status_code=400, detail="Please provide a valid email address.")

    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")

    existing_user = FirestoreService.get_user_by_email(email_clean)
    if existing_user:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    user_id = f"usr_{uuid.uuid4().hex[:8]}"
    hashed_pw = hash_password(payload.password)

    new_user = {
        "user_id": user_id,
        "name": payload.name.strip(),
        "email": email_clean,
        "phone": payload.phone.strip() if payload.phone else None,
        "password_hash": hashed_pw,
        "role": "CUSTOMER",
        "addresses": [],
        "wishlist": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    FirestoreService.create_user(new_user)
    token = create_access_token({
        "sub": user_id,
        "email": email_clean,
        "role": "CUSTOMER",
        "name": payload.name.strip()
    })

    return AuthResponse(
        token=token,
        user_id=user_id,
        name=payload.name.strip(),
        email=email_clean,
        role="CUSTOMER",
        message="Account created successfully."
    )

@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest):
    """
    Authenticate customer or admin credentials and return a signed JWT access token.
    Notice: The insecure 'password123' demo bypass has been permanently removed.
    """
    email_clean = payload.email.strip().lower()
    user = FirestoreService.get_user_by_email(email_clean)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    stored_hash = user.get("password_hash", "")
    if not verify_password(payload.password, stored_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Automatic password upgrade: If password was stored with legacy SHA-256, upgrade to Argon2id
    if not stored_hash.startswith("$argon2"):
        new_argon_hash = hash_password(payload.password)
        FirestoreService.update_user(email_clean, {"password_hash": new_argon_hash})
        logger.info(f"Upgraded password hash to Argon2id for user {email_clean}")

    role = user.get("role", "CUSTOMER")
    user_id = user.get("user_id", f"usr_{uuid.uuid4().hex[:8]}")
    name = user.get("name", "Member")

    token = create_access_token({
        "sub": user_id,
        "email": email_clean,
        "role": role,
        "name": name
    })

    return AuthResponse(
        token=token,
        user_id=user_id,
        name=name,
        email=email_clean,
        role=role,
        message="Signed in successfully."
    )

@router.post("/google", response_model=AuthResponse)
def google_auth(payload: GoogleAuthRequest):
    """
    Authenticate or register customer via Google Sign-In.
    """
    email = payload.email.strip().lower() if payload.email else ""
    name = (payload.name or "Atelier Member").strip()

    if payload.credential:
        try:
            import jwt
            decoded = jwt.decode(payload.credential, options={"verify_signature": False})
            email = decoded.get("email", email).strip().lower()
            name = decoded.get("name", name).strip()
        except Exception as e:
            logger.warning(f"Error parsing Google credential JWT: {e}")

    if not email or "@" not in email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A valid Google email address is required."
        )

    user = FirestoreService.get_user_by_email(email)
    if not user:
        user_id = f"usr_{uuid.uuid4().hex[:8]}"
        new_user = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "role": "CUSTOMER",
            "addresses": [],
            "wishlist": [],
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        FirestoreService.create_user(new_user)
        user = new_user
    else:
        user_id = user.get("user_id", f"usr_{uuid.uuid4().hex[:8]}")
        name = user.get("name") or name

    role = user.get("role", "CUSTOMER")
    token = create_access_token({
        "sub": user_id,
        "email": email,
        "role": role,
        "name": name
    })

    return AuthResponse(
        token=token,
        user_id=user_id,
        name=name,
        email=email,
        role=role,
        message=f"Welcome, {name}! Signed in with Google."
    )

@router.post("/admin-login", response_model=AuthResponse)
def admin_login(payload: LoginRequest):
    """
    Dedicated login endpoint for the Admin Management Portal.
    Verifies credentials and strictly enforces role == 'ADMIN'.
    """
    email_clean = payload.email.strip().lower()
    user = FirestoreService.get_user_by_email(email_clean)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid administrative credentials."
        )

    stored_hash = user.get("password_hash", "")
    if not verify_password(payload.password, stored_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid administrative credentials."
        )

    role = user.get("role", "").upper()
    if role != "ADMIN":
        logger.warning(f"Customer {email_clean} attempted unauthorized login to Admin Portal.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Administrator privileges required."
        )

    user_id = user.get("user_id", f"usr_{uuid.uuid4().hex[:8]}")
    name = user.get("name", "Administrator")

    token = create_access_token({
        "sub": user_id,
        "email": email_clean,
        "role": "ADMIN",
        "name": name
    })

    FirestoreService.log_admin_action(email_clean, "Logged in to Admin Management Portal")

    return AuthResponse(
        token=token,
        user_id=user_id,
        name=name,
        email=email_clean,
        role="ADMIN",
        message="Admin authentication successful."
    )

@router.post("/bootstrap-admin", response_model=AuthResponse)
def bootstrap_admin(payload: BootstrapAdminRequest):
    """
    Secure Administrator Bootstrap Process.
    Allowed only if zero admin accounts exist in the database, OR if a matching
    ADMIN_BOOTSTRAP_KEY is supplied. Prevents unauthorized hardcoded backdoors.
    """
    total_admins = FirestoreService.count_admins()
    valid_key = ADMIN_BOOTSTRAP_KEY and (payload.bootstrap_key == ADMIN_BOOTSTRAP_KEY)

    if total_admins > 0 and not valid_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator account already initialized. Bootstrap disabled."
        )

    email_clean = payload.email.strip().lower()
    existing_user = FirestoreService.get_user_by_email(email_clean)
    user_id = existing_user.get("user_id") if existing_user else f"adm_{uuid.uuid4().hex[:8]}"

    admin_data = {
        "user_id": user_id,
        "name": payload.name.strip(),
        "email": email_clean,
        "password_hash": hash_password(payload.password),
        "role": "ADMIN",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "bootstrap_initialized": True
    }

    if existing_user:
        FirestoreService.update_user(email_clean, admin_data)
    else:
        FirestoreService.create_user(admin_data)

    logger.info(f"Admin account bootstrapped: {email_clean}")
    token = create_access_token({
        "sub": user_id,
        "email": email_clean,
        "role": "ADMIN",
        "name": payload.name.strip()
    })

    return AuthResponse(
        token=token,
        user_id=user_id,
        name=payload.name.strip(),
        email=email_clean,
        role="ADMIN",
        message="Primary administrator initialized successfully."
    )

@router.get("/me")
def get_current_user_profile(user: Dict[str, Any] = Depends(get_current_user)):
    """Retrieve verified profile of the currently signed-in user."""
    safe_profile = dict(user)
    safe_profile.pop("password_hash", None)
    return {
        "authenticated": True,
        "user": safe_profile
    }

@router.put("/profile")
def update_profile(payload: ProfileUpdateRequest, user: Dict[str, Any] = Depends(require_customer)):
    """Update profile details (name, phone, delivery addresses)."""
    update_data = {}
    if payload.name:
        update_data["name"] = payload.name.strip()
    if payload.phone:
        update_data["phone"] = payload.phone.strip()
    if payload.addresses is not None:
        update_data["addresses"] = payload.addresses

    updated = FirestoreService.update_user(user["email"], update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found.")
    
    updated.pop("password_hash", None)
    return {"message": "Profile updated successfully.", "user": updated}

# =============================================================================
# WISHLIST ENDPOINTS
# =============================================================================

@router.get("/wishlist")
def get_wishlist(user: Dict[str, Any] = Depends(require_customer)):
    """Retrieve full product details for items in the customer's wishlist."""
    product_ids = FirestoreService.get_user_wishlist(user["email"])
    products = []
    for pid in product_ids:
        p = FirestoreService.get_product(pid)
        if p:
            products.append(p.model_dump())
    return {"product_ids": product_ids, "products": products}

@router.post("/wishlist/{product_id}")
def add_to_wishlist(product_id: str, user: Dict[str, Any] = Depends(require_customer)):
    """Add a product to the customer's personal wishlist."""
    product = FirestoreService.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found.")
    
    updated_wl = FirestoreService.add_to_wishlist(user["email"], product_id)
    return {"message": "Added to wishlist.", "wishlist": updated_wl}

@router.delete("/wishlist/{product_id}")
def remove_from_wishlist(product_id: str, user: Dict[str, Any] = Depends(require_customer)):
    """Remove a product from the customer's personal wishlist."""
    updated_wl = FirestoreService.remove_from_wishlist(user["email"], product_id)
    return {"message": "Removed from wishlist.", "wishlist": updated_wl}
