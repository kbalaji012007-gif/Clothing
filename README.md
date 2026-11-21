# 🌟 ATELIER — Luxury Couture & Streetwear E-Commerce Platform

[![Frontend Deployed on Vercel](https://img.shields.io/badge/Vercel-Frontend%20Live-black?style=for-the-badge&logo=vercel)](https://clothing-two-lime.vercel.app/)
[![Backend Deployed on Render](https://img.shields.io/badge/Render-Backend%20Live-46E3B7?style=for-the-badge&logo=render)](https://clothing-z77b.onrender.com/)
[![Database](https://img.shields.io/badge/Firestore-Connected-FFA000?style=for-the-badge&logo=firebase)](https://clothing-agency-atelier.firebaseapp.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi)](https://clothing-z77b.onrender.com/docs)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)](https://python.org)

**ATELIER** is an enterprise-grade luxury streetwear and high-fashion e-commerce platform. It features an interactive 3D Sneaker Orbit, Parabolic Clothing Rack, Runway Lookbook, Dual-Portal RBAC architecture (Customer Storefront + Executive Admin HQ), instant UPI payment reconciliation with 12-digit UTR validation, and authoritative backend pricing powered by Cloud Firestore.

---

## 🌐 Live Production Deployments

| Component | Production URL | Description |
|---|---|---|
| **🛍️ Customer Storefront** | [https://clothing-two-lime.vercel.app/](https://clothing-two-lime.vercel.app/) | Interactive 3D shopping experience, runway catalog, and instant bag checkout |
| **⚡ Admin Management Portal** | [https://clothing-two-lime.vercel.app/admin/dashboard.html](https://clothing-two-lime.vercel.app/admin/dashboard.html) | Product pricing, inventory, order fulfillment, and UPI reconciliation queue |
| **🔒 Customer Account Portal** | [https://clothing-two-lime.vercel.app/account/dashboard.html](https://clothing-two-lime.vercel.app/account/dashboard.html) | Member dashboard, order history, address book, and wishlist |
| **🚀 FastAPI Backend API** | [https://clothing-z77b.onrender.com/](https://clothing-z77b.onrender.com/) | High-performance Python backend deployed on Render |
| **📖 Interactive API Docs** | [https://clothing-z77b.onrender.com/docs](https://clothing-z77b.onrender.com/docs) | Live interactive Swagger UI for API exploration and testing |
| **🩺 API Health Check** | [https://clothing-z77b.onrender.com/api/health](https://clothing-z77b.onrender.com/api/health) | Live service status and database connectivity monitor |

---

## ✨ Key Architectural Highlights

### 1. Real-Time Price Synchronization & Anti-Tampering Engine
- **Instant Storefront Synchronization:** When administrators update product prices via `/admin/products.html`, changes persist to Cloud Firestore and instantly hydrate active customer sessions without page reloads.
- **Authoritative Price Enforcement:** All orders placed via `/api/orders` or `/api/upi/submit-utr` recalculate totals against server database records. Client-side price tampering triggers strict `HTTP 400 Bad Request` rejections.
- **Cart Re-validation & Notification:** Shopping bags automatically refresh item pricing upon drawer open or checkout, notifying patrons if prices changed while in the cart.

### 2. Immersive 3D Frontend Physics
- **3D Sneaker Orbit (Screen 3):** Smooth continuous spline trajectory physics, draggable jog wheel inertia, and background colorway tint transitions.
- **Parabolic Clothing Rack (Screen 2):** 3D hanging drape cable physics, garment hover elevation, and interactive quick-look modals.
- **Runway Lookbook (Screen 1):** High-fashion editorial grid layout with seamless outfit aggregation.

### 3. Integrated UPI Payment Gateway & Reconciliation Queue
- **Dynamic UPI Intent & QR Generation:** Canonical `upi://pay` generation with payee `atelier@upi`, dynamic amount in `INR`, and one-click app switches (Google Pay, PhonePe, Paytm).
- **12-Digit Numeric UTR Verification:** Validates standard reference codes, prevents duplicate UTR reuse across orders, and maintains an administrative reconciliation queue (`/admin/payments.html`).
- **On-Demand GST Invoicing:** Real-time generation of GST-compliant tax invoices for all completed transactions.

---

## 🛠️ Technology Stack

```
Frontend (Vercel)                    Backend (Render)                    Database
┌─────────────────────────┐          ┌─────────────────────────┐         ┌─────────────────────────┐
│ • Vite 8 + React 19     │  HTTPS   │ • Python 3.11 + FastAPI │  gRPC   │ • Google Cloud Firestore│
│ • Tailwind CSS v4       │ ───────> │ • Uvicorn ASGI Server   │ ──────> │ • Firebase Admin SDK    │
│ • Motion + Canvas Physics│ (Proxied)│ • PyJWT + Argon2id Auth │         │ • Native NoSQL Document │
│ • Dual-Portal Vanilla JS│          │ • Multi-Currency Engine │         │   Collections           │
└─────────────────────────┘          └─────────────────────────┘         └─────────────────────────┘
```

---

## 💻 Local Development Setup

### 1. Prerequisites
- **Node.js** (v18 or higher)
- **Python** (v3.10, v3.11, or v3.12)
- **Git**

### 2. Clone Repository
```bash
git clone https://github.com/kbalaji012007-gif/Clothing.git
cd Clothing
```

### 3. Backend Setup (FastAPI)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install Python dependencies
pip install -r backend/requirements.txt

# Start backend server (runs on port 8001)
uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
```

### 4. Frontend Setup (Vite)
```bash
# Install frontend dependencies (with aligned peer dependencies)
npm install

# Start Vite development server (runs on port 5000)
npm run dev
```

Visit **`http://localhost:5000/`** to view the live local store.

---

## 📡 Core API Reference

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/health` | Service health & Firebase status | Public |
| `GET` | `/api/products` | Retrieve store product catalog | Public |
| `GET` | `/api/products/{id}` | Get individual product details | Public |
| `PUT` | `/api/admin/products/{id}` | Update product pricing or inventory | Admin |
| `POST` | `/api/admin/products` | Create new product | Admin |
| `POST` | `/api/auth/login` | Authenticate customer credentials | Public |
| `POST` | `/api/auth/admin-login` | Authenticate administrator console | Public |
| `POST` | `/api/orders` | Place validated order | Optional |
| `POST` | `/api/upi/create-intent` | Generate UPI QR code & intent links | Public |
| `POST` | `/api/upi/submit-utr` | Submit 12-digit UTR for treasury review | Public |
| `POST` | `/api/admin/payments/{id}/verify`| Approve or reject UPI payment | Admin |

---

## 📄 License & Attribution

Designed and engineered for **ATELIER Luxury Studio**.  
All rights reserved © 2026 Atelier Couture & Streetwear Ltd.
