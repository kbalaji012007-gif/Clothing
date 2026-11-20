# Clothing Agency — Frontend Architecture

This folder contains the modularized frontend client for the Atelier digital flagship store.

---

## 📂 Structure

- **`index.html`** — Primary storefront with the **3D Parabolic Clothing Rack**, **Infinite Sneaker Orbit Showcase**, and **Runway Lookbook**.
- **`login.html`** — Member authentication (Sign In / Register) and authenticated profile card.
- **`styles/`**:
  - `store.css` — Core typography, Sneaker Orbit 3D perspective styles, and responsive layout.
  - `runway.css` — Lookbook interactive overlay, pins, and shopping bag dialog styles.
- **`scripts/`**:
  - `store.js` — 60fps spring physics loop for the curved clothing rack and modular orbit scrubber.
  - `runway.js` — Unified bag manager (`AtelierCart`), checkout controller, and lookbook interactions.
- **`services/`**:
  - `api.js` — Reusable REST client connecting frontend to backend endpoints.

---

## 🚀 Running the Frontend

The frontend is served via Vite at **`http://localhost:5000/`**.
```bash
npm run dev
```
