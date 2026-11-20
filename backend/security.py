import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
from fastapi import Header, HTTPException, status, Depends
from .config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_MINUTES, logger

# Initialize Argon2id password hasher (OWASP recommended parameters)
_password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16
)

def hash_password(password: str) -> str:
    """Hash password using Argon2id."""
    return _password_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plain password against hashed password.
    Supports Argon2id with automatic backward compatibility for legacy SHA-256 hashes.
    """
    if not hashed_password:
        return False

    # 1. Argon2id check
    if hashed_password.startswith("$argon2"):
        try:
            return _password_hasher.verify(hashed_password, plain_password)
        except (VerifyMismatchError, VerificationError, InvalidHashError):
            return False
        except Exception as e:
            logger.warning(f"Argon2 verification exception: {e}")
            return False

    # 2. Legacy SHA-256 check (for existing accounts during migration)
    legacy_sha = hashlib.sha256(plain_password.encode()).hexdigest()
    if hashed_password == legacy_sha:
        return True

    return False

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": now,
        "iss": "atelier-luxury-api"
    })
    
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and cryptographically verify a JWT access token."""
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            issuer="atelier-luxury-api"
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )

def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    FastAPI dependency: Extracts Bearer token from header, validates JWT,
    and returns authenticated user dictionary.
    """
    from .services.firestore_service import FirestoreService

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header. Bearer token required.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    parts = authorization.strip().split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected 'Bearer <token>'.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = parts[1]
    payload = decode_access_token(token)

    email = payload.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload is missing user email claim.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = FirestoreService.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account referenced in token no longer exists.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user

def get_optional_current_user(authorization: Optional[str] = Header(None)) -> Optional[Dict[str, Any]]:
    """Extracts user if Authorization header is present and valid; otherwise returns None."""
    if not authorization:
        return None
    try:
        return get_current_user(authorization)
    except Exception:
        return None

def require_customer(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Ensures caller has at least CUSTOMER role or ADMIN role."""
    role = current_user.get("role", "CUSTOMER").upper()
    if role not in ["CUSTOMER", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Customer account required."
        )
    return current_user

def require_admin(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Ensures caller has administrative privileges (ADMIN role)."""
    role = current_user.get("role", "").upper()
    if role != "ADMIN":
        logger.warning(f"Unauthorized admin access attempt by {current_user.get('email')} (role: {role})")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Administrator privileges required."
        )
    return current_user
