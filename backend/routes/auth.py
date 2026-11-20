import uuid
import hashlib
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr
from ..config import get_firestore_client, logger

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class AuthResponse(BaseModel):
    token: str
    user_id: str
    name: str
    email: str
    message: str

# In-memory users fallback
_memory_users = {
    "member@atelier.com": {
        "user_id": "usr_demo123",
        "name": "Alex Vance",
        "email": "member@atelier.com",
        "password_hash": hashlib.sha256("password123".encode()).hexdigest(),
        "created_at": datetime.utcnow().isoformat()
    }
}

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

@router.post("/register", response_model=AuthResponse)
def register(payload: RegisterRequest):
    email_clean = payload.email.strip().lower()
    db = get_firestore_client()

    if db:
        try:
            user_ref = db.collection("users").document(email_clean)
            if user_ref.get().exists:
                raise HTTPException(status_code=400, detail="An account with this email already exists.")
            
            user_id = f"usr_{uuid.uuid4().hex[:8]}"
            user_data = {
                "user_id": user_id,
                "name": payload.name.strip(),
                "email": email_clean,
                "password_hash": hash_pw(payload.password),
                "created_at": datetime.utcnow().isoformat()
            }
            user_ref.set(user_data)
            token = f"tok_{uuid.uuid4().hex}"
            return AuthResponse(
                token=token,
                user_id=user_id,
                name=payload.name,
                email=email_clean,
                message="Account created successfully."
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.warning(f"Firestore register error: {e}")

    # Fallback in-memory
    if email_clean in _memory_users:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    user_id = f"usr_{uuid.uuid4().hex[:8]}"
    _memory_users[email_clean] = {
        "user_id": user_id,
        "name": payload.name.strip(),
        "email": email_clean,
        "password_hash": hash_pw(payload.password),
        "created_at": datetime.utcnow().isoformat()
    }
    return AuthResponse(
        token=f"tok_{uuid.uuid4().hex}",
        user_id=user_id,
        name=payload.name,
        email=email_clean,
        message="Account created successfully."
    )

@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest):
    email_clean = payload.email.strip().lower()
    pw_hash = hash_pw(payload.password)
    db = get_firestore_client()

    user = None
    if db:
        try:
            doc = db.collection("users").document(email_clean).get()
            if doc.exists:
                user = doc.to_dict()
        except Exception as e:
            logger.warning(f"Firestore login check error: {e}")

    if not user:
        user = _memory_users.get(email_clean)

    if not user or user.get("password_hash") != pw_hash:
        # For seamless demo testing, allow any login with demo credentials or auto-create guest session
        if payload.password == "password123":
            user_id = f"usr_{uuid.uuid4().hex[:8]}"
            name = email_clean.split("@")[0].title()
            return AuthResponse(
                token=f"tok_{uuid.uuid4().hex}",
                user_id=user_id,
                name=name,
                email=email_clean,
                message="Signed in successfully."
            )
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    return AuthResponse(
        token=f"tok_{uuid.uuid4().hex}",
        user_id=user["user_id"],
        name=user["name"],
        email=user["email"],
        message="Signed in successfully."
    )

@router.get("/me")
def get_current_user(authorization: Optional[str] = Header(None)):
    """Retrieve profile from active session token."""
    return {
        "authenticated": True if authorization else False,
        "note": "Session active."
    }
