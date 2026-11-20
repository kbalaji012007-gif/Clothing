/**
 * Atelier Customer Account Portal Core Script
 */

const API_BASE = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://127.0.0.1:8001/api'
  : '/api';

const AccountApp = {
  getToken() {
    return localStorage.getItem('atelier_token');
  },

  getUser() {
    try {
      const raw = localStorage.getItem('atelier_user');
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  },

  setSession(token, user) {
    localStorage.setItem('atelier_token', token);
    localStorage.setItem('atelier_user', JSON.stringify(user));
  },

  clearSession() {
    localStorage.removeItem('atelier_token');
    localStorage.removeItem('atelier_user');
  },

  requireAuth() {
    const token = this.getToken();
    if (!token) {
      window.location.href = '/account/login.html';
      return false;
    }
    return true;
  },

  async apiRequest(endpoint, options = {}) {
    const token = this.getToken();
    const headers = options.headers || {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    if (!headers['Content-Type'] && options.body && typeof options.body === 'string') {
      headers['Content-Type'] = 'application/json';
    }

    const res = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers
    });

    if (res.status === 401) {
      // Session expired
      this.clearSession();
      window.location.href = '/account/login.html';
      throw new Error('Session expired. Please log in again.');
    }

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data.detail || `Request failed with status ${res.status}`);
    }
    return data;
  },

  showToast(message, isError = false) {
    let toast = document.getElementById('account-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'account-toast';
      toast.className = 'toast-notice';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.style.background = isError ? '#991b1b' : '#111111';
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3200);
  },

  initSidebar() {
    const user = this.getUser();
    if (!user) return;

    const nameEl = document.getElementById('user-sidebar-name');
    const emailEl = document.getElementById('user-sidebar-email');
    const avatarEl = document.getElementById('user-sidebar-avatar');

    if (nameEl) nameEl.textContent = user.name || 'Member';
    if (emailEl) emailEl.textContent = user.email || '';
    if (avatarEl) {
      const parts = (user.name || 'MB').trim().split(' ');
      const initials = parts.length > 1 ? (parts[0][0] + parts[parts.length - 1][0]).toUpperCase() : (user.name || 'M').substring(0, 2).toUpperCase();
      avatarEl.textContent = initials;
    }

    // Set active link based on current path
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar-link').forEach(link => {
      if (link.getAttribute('href') && currentPath.includes(link.getAttribute('href'))) {
        link.classList.add('active');
      }
    });

    // Sign out button
    const logoutBtn = document.getElementById('btn-logout');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        this.clearSession();
        window.location.href = '/account/login.html';
      });
    }
  }
};
