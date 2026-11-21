/**
 * Atelier Luxury Management Portal Core Script
 */

const ADMIN_API_BASE = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://127.0.0.1:8001/api'
  : '/api';

const AdminApp = {
  getToken() {
    return localStorage.getItem('atelier_admin_token') || localStorage.getItem('atelier_token');
  },

  getUser() {
    try {
      const raw = localStorage.getItem('atelier_admin_user') || localStorage.getItem('atelier_user');
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  },

  setSession(token, user) {
    localStorage.setItem('atelier_admin_token', token);
    localStorage.setItem('atelier_admin_user', JSON.stringify(user));
  },

  logout() {
    localStorage.removeItem('atelier_admin_token');
    localStorage.removeItem('atelier_admin_user');
    window.location.href = '/account/login.html';
  },

  requireAdmin() {
    const token = this.getToken();
    const user = this.getUser();

    if (!token || !user) {
      window.location.href = '/account/login.html';
      return false;
    }

    if (user.role !== 'ADMIN') {
      alert('Access Denied: Administrator role required.');
      this.logout();
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

    const res = await fetch(`${ADMIN_API_BASE}${endpoint}`, {
      ...options,
      headers
    });

    if (res.status === 401 || res.status === 403) {
      const data = await res.json().catch(() => ({}));
      if (res.status === 403) {
        throw new Error(data.detail || 'Access forbidden: Administrator privileges required.');
      }
      this.logout();
      throw new Error('Administrative session expired. Please sign in again.');
    }

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data.detail || `Request failed with status ${res.status}`);
    }
    return data;
  },

  showToast(message, isError = false) {
    let toast = document.getElementById('admin-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'admin-toast';
      toast.className = 'admin-toast';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.style.borderColor = isError ? 'rgba(239, 68, 68, 0.5)' : 'var(--admin-border)';
    toast.style.background = isError ? '#2a1215' : 'var(--admin-bg-card)';
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3400);
  },

  initSidebar() {
    const user = this.getUser();
    if (!user) return;

    const nameEl = document.getElementById('admin-profile-name');
    const roleEl = document.getElementById('admin-profile-role');
    const avatarEl = document.getElementById('admin-profile-avatar');

    if (nameEl) nameEl.textContent = user.name || 'Administrator';
    if (roleEl) roleEl.textContent = user.email || 'Admin';
    if (avatarEl) {
      const initials = (user.name || 'AD').substring(0, 2).toUpperCase();
      avatarEl.textContent = initials;
    }

    // Highlight active sidebar navigation
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
      const href = link.getAttribute('href');
      if (href && currentPath.includes(href) && href !== '/admin/') {
        link.classList.add('active');
      } else if (href === '/admin/dashboard.html' && (currentPath === '/admin/' || currentPath === '/admin/index.html')) {
        link.classList.add('active');
      }
    });

    // Logout trigger
    const logoutBtn = document.getElementById('admin-logout-btn');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        this.logout();
      });
    }
  }
};
