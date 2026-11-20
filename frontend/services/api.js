/**
 * Frontend REST API Service
 * Connects the UI to the Python FastAPI backend & Firebase Cloud Firestore.
 */

const API_BASE_URL = 'http://127.0.0.1:8001/api';

export const ApiService = {
  // --- Products ---
  async getProducts(category = null, search = null) {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (search) params.append('search', search);
    const res = await fetch(`${API_BASE_URL}/products?${params.toString()}`);
    if (!res.ok) throw new Error('Failed to fetch products');
    return res.json();
  },

  async getProduct(productId) {
    const res = await fetch(`${API_BASE_URL}/products/${productId}`);
    if (!res.ok) throw new Error('Product not found');
    return res.json();
  },

  // --- Cart & Shopping Bag ---
  async getCart(sessionId = 'guest_session') {
    const res = await fetch(`${API_BASE_URL}/cart/${sessionId}`);
    if (!res.ok) throw new Error('Failed to fetch cart');
    return res.json();
  },

  async addToCart(sessionId = 'guest_session', productId, size = 'M', quantity = 1) {
    const res = await fetch(`${API_BASE_URL}/cart/${sessionId}/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: productId, size, quantity })
    });
    if (!res.ok) throw new Error('Failed to add item to cart');
    return res.json();
  },

  async removeFromCart(sessionId = 'guest_session', itemId) {
    const res = await fetch(`${API_BASE_URL}/cart/${sessionId}/items/${itemId}`, {
      method: 'DELETE'
    });
    if (!res.ok) throw new Error('Failed to remove item');
    return res.json();
  },

  // --- Orders & Checkout ---
  async createOrder(orderPayload) {
    const res = await fetch(`${API_BASE_URL}/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(orderPayload)
    });
    if (!res.ok) throw new Error('Failed to place order');
    return res.json();
  },

  async getOrder(orderId) {
    const res = await fetch(`${API_BASE_URL}/orders/${orderId}`);
    if (!res.ok) throw new Error('Order not found');
    return res.json();
  },

  // --- Authentication ---
  async login(email, password) {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Login failed');
    return data;
  },

  async register(name, email, password) {
    const res = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Registration failed');
    return data;
  }
};
