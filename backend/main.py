from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import PORT, HOST, CORS_ORIGINS, is_firebase_connected, logger, ADMIN_EMAIL, ADMIN_INITIAL_PASSWORD
from .routes import products_router, cart_router, orders_router, auth_router, upi_router, admin_router
from .services.firestore_service import FirestoreService
from .security import hash_password

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Seed initial products into Firestore or memory
    logger.info("Initializing Clothing Agency API Backend...")
    count = FirestoreService.seed_products_if_empty()
    logger.info(f"Products initialized ({count} products loaded).")

    # Bootstrap administrator if credentials provided in environment
    if ADMIN_EMAIL and ADMIN_INITIAL_PASSWORD:
        admin_user = FirestoreService.get_user_by_email(ADMIN_EMAIL)
        if not admin_user:
            FirestoreService.create_user({
                "user_id": "adm_master_001",
                "name": "Atelier Master Administrator",
                "email": ADMIN_EMAIL.strip().lower(),
                "password_hash": hash_password(ADMIN_INITIAL_PASSWORD),
                "role": "ADMIN"
            })
            logger.info(f"Primary Administrator provisioned: {ADMIN_EMAIL}")
        else:
            from .security import verify_password
            if not verify_password(ADMIN_INITIAL_PASSWORD, admin_user.get("password_hash", "")) or admin_user.get("role") != "ADMIN":
                FirestoreService.update_user(ADMIN_EMAIL, {
                    "password_hash": hash_password(ADMIN_INITIAL_PASSWORD),
                    "role": "ADMIN"
                })
                logger.info(f"Synchronized administrator credentials for: {ADMIN_EMAIL}")

    yield
    logger.info("Shutting down Clothing Agency API Backend.")

app = FastAPI(
    title="Clothing Agency E-Commerce API",
    description="Python FastAPI backend with Dual-Portal Architecture (Customer & Admin), JWT RBAC, and Firestore integration.",
    version="2.0.0",
    lifespan=lifespan
)

# CORS configuration allowing requests from the frontend Vite server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(products_router, prefix="/api")
app.include_router(cart_router, prefix="/api")
app.include_router(orders_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(upi_router, prefix="/api")
app.include_router(admin_router, prefix="/api")

@app.get("/api/health", tags=["Health"])
def health_check():
    """Health status and Firebase connectivity information."""
    firebase_status = "connected" if is_firebase_connected() else "development_memory_mode"
    products = FirestoreService.get_all_products()
    return {
        "status": "healthy",
        "service": "clothing-agency-api",
        "firebase_status": firebase_status,
        "total_products": len(products),
        "docs_url": "/docs"
    }

@app.post("/api/seed", tags=["Seed"])
def trigger_seed():
    """Seed or re-sync catalog products into Firestore."""
    count = FirestoreService.seed_products_if_empty()
    return {"message": "Catalog products seeded successfully", "count": count}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
