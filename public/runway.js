(function () {
  'use strict';

  const STORAGE_KEY = 'runway-styling-bag-v3';
  const ASSET_BASE = 'https://reel-ref-try-the-look.vercel.app/assets/';

  const NATIVE_CATALOG = {
    source: '#runway',
    looks: [
      {
        name: 'The City Edit',
        description: 'A charcoal knit and easy denim.',
        image: ASSET_BASE + 'original-look-1.webp',
        products: ['tatum-5-orbit-copy', 'tshirt', 'sweatshirt']
      },
      {
        name: 'Gallery Opening',
        description: 'A clean white tee and relaxed denim.',
        image: ASSET_BASE + 'original-look-5.webp',
        products: ['tatum-5-orbit', 'hoodie-black', 'tshirt']
      },
      {
        name: 'Gallery Opening',
        description: 'Olive knitwear. A grounded palette.',
        image: ASSET_BASE + 'original-look-4.webp',
        products: ['sweatshirt-plus', 'tatum-5-orbit', 'tshirt']
      },
      {
        name: 'Studio Day',
        description: 'Black, white and laid-back denim.',
        image: ASSET_BASE + 'original-look-6.webp',
        products: ['hoodie-black', 'tatum-5-orbit-copy', 'tshirt']
      },
      {
        name: 'Studio Day',
        description: 'Burgundy layers. A tailored perspective.',
        image: ASSET_BASE + 'original-look-3.webp',
        products: ['sweatshirt', 'tatum-5-orbit', 'tshirt']
      },
      {
        name: 'Studio Day',
        description: 'A grey crew and your favourite denim.',
        image: ASSET_BASE + 'original-look-2.webp',
        products: ['hoodie', 'air-jordan-12-retro-copy', 'tshirt']
      }
    ],
    items: [
      {
        id: 'tatum-5-orbit-copy',
        name: 'Air Jordan 12 Retro',
        type: 'From the original lookbook',
        price: 149.0,
        image: ASSET_BASE + 'source-tatum-5-orbit-copy.webp',
        sizes: ['40', '41', '42', '43', '44', '45', '46'],
        variants: [
          { id: 57015167025457, a: true, o: ['40'] },
          { id: 57015167058225, a: true, o: ['41'] },
          { id: 57015167090993, a: true, o: ['42'] },
          { id: 57015167123761, a: true, o: ['43'] },
          { id: 57015167156529, a: true, o: ['44'] },
          { id: 57015167189297, a: true, o: ['45'] },
          { id: 57015167222065, a: true, o: ['46'] }
        ],
        url: '#details'
      },
      {
        id: 'tshirt',
        name: 'Tshirt',
        type: 'From the original lookbook',
        price: 199.0,
        image: ASSET_BASE + 'source-tshirt.webp',
        sizes: ['S', 'L', 'M', 'XL'],
        variants: [
          { id: 56835911582001, a: true, o: ['S'] },
          { id: 56835911614769, a: true, o: ['L'] },
          { id: 56835911647537, a: true, o: ['M'] },
          { id: 56835911680305, a: true, o: ['XL'] }
        ],
        url: '#details'
      },
      {
        id: 'sweatshirt',
        name: 'Sweatshirt',
        type: 'From the original lookbook',
        price: 199.0,
        image: ASSET_BASE + 'source-sweatshirt.webp',
        sizes: ['S', 'L', 'M', 'XL'],
        variants: [
          { id: 56835806396721, a: true, o: ['S'] },
          { id: 56835806429489, a: true, o: ['L'] },
          { id: 56835806462257, a: true, o: ['M'] },
          { id: 56835806495025, a: true, o: ['XL'] }
        ],
        url: '#details'
      },
      {
        id: 'tatum-5-orbit',
        name: 'Tatum 5 Orbit',
        type: 'From the original lookbook',
        price: 149.0,
        image: ASSET_BASE + 'source-tatum-5-orbit.webp',
        sizes: ['40', '41', '42', '43', '44', '45', '46'],
        variants: [
          { id: 57015166730545, a: true, o: ['40'] },
          { id: 57015166763313, a: true, o: ['41'] },
          { id: 57015166796081, a: true, o: ['42'] },
          { id: 57015166828849, a: true, o: ['43'] },
          { id: 57015166861617, a: true, o: ['44'] },
          { id: 57015166894385, a: true, o: ['45'] },
          { id: 57015166927153, a: true, o: ['46'] }
        ],
        url: '#details'
      },
      {
        id: 'hoodie-black',
        name: 'Hoodie Black',
        type: 'From the original lookbook',
        price: 199.0,
        image: ASSET_BASE + 'source-hoodie-black.webp',
        sizes: ['S', 'L', 'M', 'XL'],
        variants: [
          { id: 56836251681073, a: true, o: ['S'] },
          { id: 56836251713841, a: true, o: ['L'] },
          { id: 56836251746609, a: true, o: ['M'] },
          { id: 56836251779377, a: true, o: ['XL'] }
        ],
        url: '#details'
      },
      {
        id: 'sweatshirt-plus',
        name: 'Sweatshirt Plus',
        type: 'From the original lookbook',
        price: 199.0,
        image: ASSET_BASE + 'source-sweatshirt-plus.webp',
        sizes: ['S', 'L', 'M', 'XL'],
        variants: [
          { id: 56836143743281, a: true, o: ['S'] },
          { id: 56836143776049, a: true, o: ['L'] },
          { id: 56836143808817, a: true, o: ['M'] },
          { id: 56836143841585, a: true, o: ['XL'] }
        ],
        url: '#details'
      },
      {
        id: 'hoodie',
        name: 'Hoodie',
        type: 'From the original lookbook',
        price: 199.0,
        image: ASSET_BASE + 'source-hoodie.webp',
        sizes: ['S', 'L', 'M', 'XL'],
        variants: [
          { id: 56836002185521, a: true, o: ['S'] },
          { id: 56836002218289, a: true, o: ['L'] },
          { id: 56836002251057, a: true, o: ['M'] },
          { id: 56836002283825, a: true, o: ['XL'] }
        ],
        url: '#details'
      },
      {
        id: 'air-jordan-12-retro-copy',
        name: 'Luka 5',
        type: 'From the original lookbook',
        price: 149.0,
        image: ASSET_BASE + 'source-air-jordan-12-retro-copy.webp',
        sizes: ['40', '41', '42', '43', '44', '45', '46'],
        variants: [
          { id: 57015176364337, a: true, o: ['40'] },
          { id: 57015176397105, a: true, o: ['41'] },
          { id: 57015176429873, a: true, o: ['42'] },
          { id: 57015176462641, a: true, o: ['43'] },
          { id: 57015176495409, a: true, o: ['44'] },
          { id: 57015176528177, a: true, o: ['45'] },
          { id: 57015176560945, a: true, o: ['46'] }
        ],
        url: '#details'
      }
    ]
  };

  function validateCatalog(cat) {
    if (!cat || !Array.isArray(cat.items)) {
      throw new Error('The product list could not load.');
    }
    const variantMap = new Map();
    for (const item of cat.items) {
      if (
        !item ||
        typeof item.id !== 'string' ||
        typeof item.name !== 'string' ||
        typeof item.price !== 'number' ||
        !Number.isFinite(item.price) ||
        item.price < 0 ||
        !Array.isArray(item.variants)
      ) {
        throw new Error('The product list is unavailable.');
      }
      for (const v of item.variants) {
        if (
          !v ||
          !Number.isSafeInteger(v.id) ||
          typeof v.a !== 'boolean' ||
          !Array.isArray(v.o) ||
          !v.o.every((o) => typeof o === 'string')
        ) {
          throw new Error('The product list is unavailable.');
        }
        variantMap.set(v.id, { item, variant: v });
      }
    }
    return { catalog: cat, variantMap };
  }

  const usd = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  });

  const { variantMap } = validateCatalog(NATIVE_CATALOG);

  function loadBag() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return [];
      const parsed = JSON.parse(raw);
      if (!Array.isArray(parsed)) return [];
      const valid = [];
      for (const entry of parsed) {
        if (entry && entry.id !== undefined) {
          const qty = Number(entry.quantity) >= 1 ? Number(entry.quantity) : 1;
          valid.push({ ...entry, quantity: qty });
          if (valid.length >= 50) break;
        }
      }
      return valid;
    } catch {
      return [];
    }
  }

  function saveBag(entries) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
    } catch {
      // Ignore storage write errors
    }
  }

  let bagEntries = loadBag();
  let toastTimer = 0;

  function updateCounters() {
    const total = bagEntries.reduce((sum, e) => sum + (Number(e.quantity) || 1), 0);
    document.querySelectorAll('[data-cart-count]').forEach((el) => {
      el.textContent = String(total);
    });
  }

  function showToast(text) {
    const status = document.getElementById('bag-status');
    if (!status) return;
    clearTimeout(toastTimer);
    status.textContent = text;
    status.classList.add('is-on');
    toastTimer = window.setTimeout(() => {
      status.classList.remove('is-on');
    }, 2500);
  }

  let selectedPaymentMethod = 'upi';
  let activeUpiOrderId = null;
  let activeOrderItems = [];
  let activeSubtotal = 0;

  function renderBagDialog() {
    const container = document.getElementById('bag-items');
    const totalEl = document.getElementById('bag-total');
    const checkoutBtn = document.getElementById('checkout-btn');
    if (!container) return;

    container.textContent = '';

    if (bagEntries.length === 0) {
      const p = document.createElement('p');
      p.className = 'bag-note';
      p.style.textAlign = 'center';
      p.style.padding = '32px 10px';
      p.style.color = '#707072';
      p.textContent = 'Your shopping bag is currently empty. Explore the Sneaker Orbit or Clothing Rack to add items.';
      container.appendChild(p);
      if (totalEl) totalEl.innerHTML = '';
      if (checkoutBtn) {
        checkoutBtn.disabled = true;
        checkoutBtn.textContent = 'Bag is Empty';
      }
      return;
    }

    let subtotal = 0;
    let totalUnits = 0;

    for (const entry of bagEntries) {
      let name, price, sizeStr, image;

      if (entry.name && entry.price !== undefined) {
        name = entry.name;
        price = Number(entry.price) || 0;
        sizeStr = entry.size ? `Size ${entry.size}` : 'Standard';
        image = entry.image || '';
      } else {
        const found = variantMap.get(entry.id);
        if (!found) continue;
        name = found.item.name;
        price = Number(found.item.price) || 0;
        sizeStr = `Size ${found.variant.o.join(' / ')}`;
        image = found.item.image;
      }

      const qty = Number(entry.quantity) || 1;
      subtotal += price * qty;
      totalUnits += qty;

      const row = document.createElement('div');
      row.className = 'bag-row';

      const img = document.createElement('img');
      img.src = image;
      img.alt = name;
      img.width = 60;
      img.height = 80;
      img.style.objectFit = 'contain';
      img.style.background = '#f9f9f9';
      img.style.borderRadius = '4px';

      const details = document.createElement('div');
      const h3 = document.createElement('h3');
      h3.textContent = name;
      h3.style.fontWeight = '600';
      h3.style.marginBottom = '4px';

      const meta = document.createElement('p');
      meta.style.fontSize = '12px';
      meta.style.color = '#666';
      meta.style.marginBottom = '4px';
      meta.textContent = `${sizeStr} · Qty: ${qty} · ${usd.format(price)} each`;

      const lineTotal = document.createElement('div');
      lineTotal.style.fontSize = '13px';
      lineTotal.style.fontWeight = '700';
      lineTotal.style.color = '#111';
      lineTotal.textContent = `Total: ${usd.format(price * qty)}`;

      details.append(h3, meta, lineTotal);

      const removeBtn = document.createElement('button');
      removeBtn.type = 'button';
      removeBtn.className = 'bag-remove';
      removeBtn.dataset.bagRemove = String(entry.id);
      removeBtn.setAttribute('aria-label', `Remove ${name}`);
      removeBtn.textContent = '×';

      row.append(img, details, removeBtn);
      container.appendChild(row);
    }

    const inrAmount = subtotal * 86.50;
    const formattedInr = '₹' + inrAmount.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    const formattedInrShort = '₹' + inrAmount.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 });

    if (totalEl) {
      totalEl.innerHTML = `
        <div style="margin-top: 16px; padding: 14px 16px; background: #fafafa; border: 1px solid #eaeaea; border-radius: 8px;">
          <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:12px; color:#666;">
            <span>Selected Products (${totalUnits} piece${totalUnits === 1 ? '' : 's'})</span>
            <span>${usd.format(subtotal)}</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:12px; color:#666;">
            <span>Courier Delivery</span>
            <span style="color:#166534; font-weight:600;">Complimentary</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:12px; color:#666;">
            <span>UPI Conversion Rate (1 USD = ₹86.50)</span>
            <span style="font-family:monospace; font-weight:600;">${formattedInr}</span>
          </div>
          <div style="display:flex; justify-content:space-between; padding-top:8px; border-top:1px solid #eaeaea; font-size:14px; font-weight:700; color:#111;">
            <span>Order Total</span>
            <span>${usd.format(subtotal)} <span style="font-size:11px; font-weight:500; color:#166534;">(${formattedInr})</span></span>
          </div>
        </div>
      `;
    }

    if (checkoutBtn) {
      checkoutBtn.disabled = bagEntries.length === 0;
      if (bagEntries.length === 0) {
        checkoutBtn.textContent = 'Bag is Empty';
      } else if (selectedPaymentMethod === 'upi') {
        checkoutBtn.textContent = `Proceed with UPI (${formattedInrShort}) →`;
      } else {
        checkoutBtn.textContent = `Instant Member Checkout (${usd.format(subtotal)}) →`;
      }
    }
  }

  const AtelierCart = {
    add(itemOrItems) {
      if (Array.isArray(itemOrItems)) {
        for (const req of itemOrItems) {
          const found = variantMap.get(req.id);
          if (!found) continue;
          const qty = Number.isSafeInteger(req.quantity) && req.quantity > 0 ? req.quantity : 1;
          const existing = bagEntries.find((e) => String(e.id) === String(req.id));
          if (existing) {
            existing.quantity = Math.min(20, (Number(existing.quantity) || 1) + qty);
          } else if (bagEntries.length < 50) {
            bagEntries.push({
              id: req.id,
              name: found.item.name,
              price: found.item.price,
              size: found.variant.o.join(' / '),
              image: found.item.image,
              quantity: Math.min(20, qty)
            });
          }
        }
      } else if (itemOrItems && typeof itemOrItems === 'object') {
        const item = itemOrItems;
        const qty = Number(item.quantity) || 1;
        const existing = bagEntries.find((e) => String(e.id) === String(item.id));
        if (existing) {
          existing.quantity = Math.min(20, (Number(existing.quantity) || 1) + qty);
        } else if (bagEntries.length < 50) {
          bagEntries.push({
            id: String(item.id),
            name: item.name || 'Product',
            price: Number(item.price) || 0,
            size: String(item.size || 'M'),
            image: item.image || '',
            quantity: Math.min(20, qty)
          });
        }
      }
      saveBag(bagEntries);
      updateCounters();
      renderBagDialog();
      const msg = Array.isArray(itemOrItems)
        ? (itemOrItems.length > 1 ? 'Look saved to your shopping bag' : 'Piece saved to your shopping bag')
        : `${itemOrItems.name} (Size ${itemOrItems.size}) added to bag`;
      showToast(msg);

      // Automatically open the shopping bag dialog so the customer immediately sees what products are in the cart
      const dialog = document.getElementById('bag-dialog');
      if (dialog && typeof dialog.showModal === 'function') {
        const contentView = document.getElementById('bag-content-view');
        const successView = document.getElementById('order-success-view');
        if (contentView) contentView.style.display = 'block';
        if (successView) successView.style.display = 'none';
        renderBagDialog();
        if (!dialog.open) {
          dialog.showModal();
        }
      }

      // Async sync to backend API if available
      try {
        const itm = Array.isArray(itemOrItems) ? itemOrItems[0] : itemOrItems;
        fetch('http://127.0.0.1:8001/api/cart/guest_session/items', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            product_id: String(itm.productId || itm.id),
            size: String(itm.size || 'M'),
            quantity: itm.quantity || 1
          })
        }).catch(() => {});
      } catch (e) {}
    },
    remove(id) {
      bagEntries = bagEntries.filter((entry) => String(entry.id) !== String(id));
      saveBag(bagEntries);
      updateCounters();
      renderBagDialog();
    },
    getItems() {
      return bagEntries;
    },
    getCount() {
      return bagEntries.reduce((sum, e) => sum + (Number(e.quantity) || 1), 0);
    }
  };

  window.AtelierCart = AtelierCart;
  window.RunwayBag = {
    add(items) {
      AtelierCart.add(items);
    }
  };

  function initBagUI() {
    updateCounters();
    const openBtn = document.getElementById('open-bag');
    const dialog = document.getElementById('bag-dialog');
    const closeBtn = document.getElementById('close-bag');
    const itemsEl = document.getElementById('bag-items');
    const checkoutBtn = document.getElementById('checkout-btn');
    const contentView = document.getElementById('bag-content-view');
    const upiView = document.getElementById('upi-checkout-view');
    const successView = document.getElementById('order-success-view');
    const continueShoppingBtn = document.getElementById('continue-shopping-btn');
    const upiBackBtn = document.getElementById('upi-back-btn');
    const copyUpiBtn = document.getElementById('copy-upi-btn');
    const confirmUtrBtn = document.getElementById('confirm-utr-btn');
    const utrInput = document.getElementById('upi-utr-input');
    const utrError = document.getElementById('utr-error');
    const payUpiPill = document.getElementById('pay-upi-pill');
    const payCardPill = document.getElementById('pay-card-pill');

    function resetDialogViews() {
      if (contentView) contentView.style.display = 'block';
      if (upiView) upiView.style.display = 'none';
      if (successView) successView.style.display = 'none';
      if (utrError) utrError.style.display = 'none';
      if (utrInput) utrInput.value = '';
      const billPrompt = document.getElementById('bill-option-prompt');
      const billCard = document.getElementById('generated-bill-card');
      if (billPrompt) billPrompt.style.display = 'block';
      if (billCard) billCard.style.display = 'none';
    }

    // Payment Method Pill Switcher
    if (payUpiPill && payCardPill) {
      payUpiPill.addEventListener('click', () => {
        selectedPaymentMethod = 'upi';
        payUpiPill.style.background = '#111';
        payUpiPill.style.color = '#fff';
        payUpiPill.style.borderColor = '#111';
        payCardPill.style.background = '#fff';
        payCardPill.style.color = '#111';
        payCardPill.style.borderColor = '#e5e5e5';
        renderBagDialog();
      });

      payCardPill.addEventListener('click', () => {
        selectedPaymentMethod = 'card';
        payCardPill.style.background = '#111';
        payCardPill.style.color = '#fff';
        payCardPill.style.borderColor = '#111';
        payUpiPill.style.background = '#fff';
        payUpiPill.style.color = '#111';
        payUpiPill.style.borderColor = '#e5e5e5';
        renderBagDialog();
      });
    }

    if (openBtn && dialog) {
      openBtn.addEventListener('click', () => {
        resetDialogViews();
        renderBagDialog();
        dialog.showModal();
      });
    }
    if (closeBtn && dialog) {
      closeBtn.addEventListener('click', () => {
        dialog.close();
        resetDialogViews();
      });
    }
    if (continueShoppingBtn && dialog) {
      continueShoppingBtn.addEventListener('click', () => {
        dialog.close();
        resetDialogViews();
      });
    }
    if (upiBackBtn) {
      upiBackBtn.addEventListener('click', () => {
        if (upiView) upiView.style.display = 'none';
        if (contentView) contentView.style.display = 'block';
      });
    }

    if (copyUpiBtn) {
      copyUpiBtn.addEventListener('click', () => {
        const vpaEl = document.getElementById('upi-vpa-text');
        const text = vpaEl ? vpaEl.textContent.trim() : 'atelier@upi';
        navigator.clipboard.writeText(text).then(() => {
          copyUpiBtn.textContent = 'Copied!';
          setTimeout(() => { copyUpiBtn.textContent = 'Copy'; }, 2000);
        }).catch(() => {
          copyUpiBtn.textContent = 'atelier@upi';
        });
      });
    }

    if (dialog) {
      dialog.addEventListener('click', (e) => {
        if (e.target !== dialog) return;
        const r = dialog.getBoundingClientRect();
        if (
          e.clientX < r.left ||
          e.clientX > r.right ||
          e.clientY < r.top ||
          e.clientY > r.bottom
        ) {
          dialog.close();
          resetDialogViews();
        }
      });
    }

    if (itemsEl) {
      itemsEl.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-bag-remove]');
        if (!btn) return;
        const removeId = String(btn.dataset.bagRemove);
        bagEntries = bagEntries.filter((entry) => String(entry.id) !== removeId);
        saveBag(bagEntries);
        updateCounters();
        renderBagDialog();
      });
    }

    // Checkout & Order Placement Handler
    if (checkoutBtn) {
      checkoutBtn.addEventListener('click', async () => {
        if (bagEntries.length === 0) return;

        // 1. Check if user is logged in
        let user = null;
        try {
          const raw = localStorage.getItem('atelier_user');
          if (raw) user = JSON.parse(raw);
        } catch (e) {}

        if (!user) {
          // If not logged in, prompt user and store pending checkout intent
          showToast('Please sign in to place your order.');
          sessionStorage.setItem('pending_checkout', 'true');
          setTimeout(() => {
            window.location.href = '/login.html';
          }, 500);
          return;
        }

        // Map items
        const orderItems = bagEntries.map((e) => {
          let name = e.name;
          let price = Number(e.price) || 0;
          let size = e.size || 'M';
          if (!name && variantMap.get(e.id)) {
            const f = variantMap.get(e.id);
            name = f.item.name;
            price = Number(f.item.price) || 0;
            size = f.variant.o.join(' / ');
          }
          return {
            product_id: String(e.productId || e.id),
            title: name || 'Piece',
            size: String(size),
            quantity: Number(e.quantity) || 1,
            price: price
          };
        });

        const subtotal = orderItems.reduce((s, i) => s + i.price * i.quantity, 0);
        activeOrderItems = orderItems;
        activeSubtotal = subtotal;

        // 2A. UPI Gateway Checkout
        if (selectedPaymentMethod === 'upi') {
          checkoutBtn.disabled = true;
          checkoutBtn.textContent = 'Connecting to UPI Gateway...';
          const orderId = 'ORD-' + Math.random().toString(36).substring(2, 8).toUpperCase();
          activeUpiOrderId = orderId;

          try {
            const res = await fetch('http://127.0.0.1:8001/api/upi/create-intent', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                orderId: orderId,
                amountUsd: subtotal,
                customerName: user.name || 'Member',
                customerEmail: user.email || 'member@atelier.com',
                items: orderItems
              })
            });

            const upiData = await res.json();
            if (contentView) contentView.style.display = 'none';
            if (upiView) upiView.style.display = 'block';

            const inrEl = document.getElementById('upi-inr-amount');
            const usdEl = document.getElementById('upi-usd-equiv');
            const qrImg = document.getElementById('upi-qr-img');
            const vpaEl = document.getElementById('upi-vpa-text');
            const gpayEl = document.getElementById('app-gpay');
            const phonepeEl = document.getElementById('app-phonepe');
            const paytmEl = document.getElementById('app-paytm');

            if (inrEl) inrEl.textContent = upiData.formattedInr || `₹${(subtotal * 86.50).toFixed(2)}`;
            if (usdEl) usdEl.textContent = `Approx. ${usd.format(subtotal)} USD`;
            if (qrImg) qrImg.src = upiData.qrImageUrl;
            if (vpaEl) vpaEl.textContent = upiData.payeeVpa || 'atelier@upi';

            if (upiData.providers) {
              if (gpayEl && upiData.providers.gpay) gpayEl.href = upiData.providers.gpay.launchUrl;
              if (phonepeEl && upiData.providers.phonepe) phonepeEl.href = upiData.providers.phonepe.launchUrl;
              if (paytmEl && upiData.providers.paytm) paytmEl.href = upiData.providers.paytm.launchUrl;
            }
          } catch (err) {
            // Local fallback intent
            if (contentView) contentView.style.display = 'none';
            if (upiView) upiView.style.display = 'block';
            const inr = subtotal * 86.50;
            const inrEl = document.getElementById('upi-inr-amount');
            const usdEl = document.getElementById('upi-usd-equiv');
            const qrImg = document.getElementById('upi-qr-img');
            if (inrEl) inrEl.textContent = '₹' + inr.toLocaleString('en-IN', { minimumFractionDigits: 2 });
            if (usdEl) usdEl.textContent = `Approx. ${usd.format(subtotal)} USD`;
            if (qrImg) qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(`upi://pay?pa=atelier@upi&pn=Atelier+Collection&am=${inr.toFixed(2)}&cu=INR&tn=Order+${orderId}`)}`;
          } finally {
            checkoutBtn.disabled = false;
            renderBagDialog();
          }
          return;
        }

        // 2B. Member Instant Card Checkout
        checkoutBtn.disabled = true;
        checkoutBtn.textContent = 'Recording Order in Firestore...';

        try {
          const res = await fetch('http://127.0.0.1:8001/api/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              customer_name: user.name || 'Member',
              customer_email: user.email || 'member@atelier.com',
              shipping_address: 'Atelier Member Express Delivery',
              items: orderItems,
              payment_method: 'member_instant_checkout'
            })
          });

          const orderData = await res.json();
          const confirmedId = orderData.id || ('ORD-' + Math.random().toString(36).substring(2, 8).toUpperCase());
          
          bagEntries = [];
          saveBag(bagEntries);
          updateCounters();
          displayOrderSuccess(confirmedId, user.name, subtotal, '💳 Member Instant Card', orderItems);
        } catch (err) {
          const fallbackId = 'ORD-' + Math.random().toString(36).substring(2, 8).toUpperCase();
          bagEntries = [];
          saveBag(bagEntries);
          updateCounters();
          displayOrderSuccess(fallbackId, user.name, subtotal, '💳 Member Instant Card', orderItems);
        }
      });
    }

    // Confirm UTR Payment Submission
    if (confirmUtrBtn && utrInput) {
      confirmUtrBtn.addEventListener('click', async () => {
        const utrVal = utrInput.value.trim();
        if (!/^\d{12}$/.test(utrVal)) {
          if (utrError) {
            utrError.textContent = 'Please enter a valid 12-digit numeric UPI reference (UTR).';
            utrError.style.display = 'block';
          }
          utrInput.focus();
          return;
        }
        if (utrError) utrError.style.display = 'none';

        let user = null;
        try {
          const raw = localStorage.getItem('atelier_user');
          if (raw) user = JSON.parse(raw);
        } catch (e) {}

        confirmUtrBtn.disabled = true;
        confirmUtrBtn.textContent = 'Verifying & Recording...';

        try {
          const res = await fetch('http://127.0.0.1:8001/api/upi/submit-utr', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              orderId: activeUpiOrderId || ('ORD-' + Math.random().toString(36).substring(2, 8).toUpperCase()),
              utr: utrVal,
              amountUsd: activeSubtotal,
              customerName: user ? user.name : 'Member',
              customerEmail: user ? user.email : 'member@atelier.com',
              items: activeOrderItems
            })
          });

          const data = await res.json();
          const confirmedId = (data.order && data.order.id) || activeUpiOrderId;
          
          bagEntries = [];
          saveBag(bagEntries);
          updateCounters();

          if (upiView) upiView.style.display = 'none';
          displayOrderSuccess(confirmedId, user ? user.name : 'Member', activeSubtotal, `⚡ UPI Verified (UTR: ${utrVal})`, activeOrderItems);
        } catch (err) {
          const fallbackId = activeUpiOrderId || ('ORD-' + Math.random().toString(36).substring(2, 8).toUpperCase());
          bagEntries = [];
          saveBag(bagEntries);
          updateCounters();
          if (upiView) upiView.style.display = 'none';
          displayOrderSuccess(fallbackId, user ? user.name : 'Member', activeSubtotal, `⚡ UPI Verified (UTR: ${utrVal})`, activeOrderItems);
        } finally {
          confirmUtrBtn.disabled = false;
          confirmUtrBtn.textContent = 'Confirm Order ✓';
        }
      });
    }

    let lastConfirmedOrder = null;

    function displayOrderSuccess(orderId, customerName, total, paymentMethod, items) {
      if (contentView) contentView.style.display = 'none';
      if (upiView) upiView.style.display = 'none';
      if (successView) successView.style.display = 'block';

      const orderItems = items && items.length > 0 ? items : [...activeOrderItems];
      lastConfirmedOrder = {
        id: orderId,
        customer: customerName || 'Member',
        total: total,
        paymentMethod: paymentMethod || '⚡ UPI Gateway (Verified)',
        items: orderItems,
        timestamp: new Date()
      };

      const orderIdEl = document.getElementById('confirmed-order-id');
      const customerEl = document.getElementById('confirmed-customer');
      const totalEl = document.getElementById('confirmed-total');
      const methodEl = document.getElementById('confirmed-payment-method');

      if (orderIdEl) orderIdEl.textContent = orderId;
      if (customerEl) customerEl.textContent = customerName || 'Member';
      if (totalEl) totalEl.textContent = usd.format(total);
      if (methodEl) methodEl.textContent = paymentMethod || '⚡ UPI Gateway (Verified)';

      // On-Demand Algorithm: Check if user explicitly required bill option
      const optBillCheckbox = document.getElementById('opt-bill-checkbox');
      const billPrompt = document.getElementById('bill-option-prompt');
      const billCard = document.getElementById('generated-bill-card');

      if (optBillCheckbox && optBillCheckbox.checked) {
        // User requested bill option beforehand
        generateBillOnDemand(orderId, lastConfirmedOrder);
      } else {
        // Default: bill is NOT generated unless requested by the user
        if (billPrompt) billPrompt.style.display = 'block';
        if (billCard) billCard.style.display = 'none';
      }

      showToast(`Order ${orderId} placed successfully!`);
    }

    async function generateBillOnDemand(orderId, orderDetails) {
      const triggerBtn = document.getElementById('trigger-generate-bill-btn');
      const billPrompt = document.getElementById('bill-option-prompt');
      const billCard = document.getElementById('generated-bill-card');

      if (triggerBtn) {
        triggerBtn.disabled = true;
        triggerBtn.innerHTML = '<span>⏳ Generating Official Bill...</span>';
      }

      try {
        const res = await fetch(`http://127.0.0.1:8001/api/orders/${orderId}/invoice`);
        const inv = await res.json();

        // Populate Bill Card Details
        const invNumEl = document.getElementById('bill-inv-number');
        const invDateEl = document.getElementById('bill-inv-date');
        const billItemsList = document.getElementById('bill-items-list');
        const billTotalsSummary = document.getElementById('bill-totals-summary');

        if (invNumEl) invNumEl.textContent = inv.invoice_number;
        if (invDateEl) invDateEl.textContent = inv.invoice_date;

        if (billItemsList) {
          billItemsList.innerHTML = inv.items.map((itm) => `
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px; padding-bottom: 6px; border-bottom: 1px dashed #eee;">
              <div>
                <strong style="color: #111;">${itm.title}</strong>
                <div style="font-size: 11px; color: #777;">Size: ${itm.size} · Qty: ${itm.quantity}</div>
              </div>
              <div style="text-align: right; font-weight: 600; color: #111;">
                $${itm.line_total_usd.toFixed(2)}
                <div style="font-size: 10px; color: #166534;">₹${itm.line_total_inr.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
              </div>
            </div>
          `).join('');
        }

        if (billTotalsSummary) {
          billTotalsSummary.innerHTML = `
            <div style="display:flex; justify-content:space-between; margin-bottom:4px; color:#666;">
              <span>Items Subtotal:</span>
              <span>$${inv.financials.subtotal_usd.toFixed(2)} (₹${inv.financials.subtotal_inr.toLocaleString('en-IN', { minimumFractionDigits: 2 })})</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:4px; color:#666;">
              <span>GST (18% included):</span>
              <span>₹${(inv.financials.cgst_inr + inv.financials.sgst_inr).toFixed(2)}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:4px; color:#666;">
              <span>Express Courier Delivery:</span>
              <span style="color:#166534; font-weight:600;">FREE</span>
            </div>
            <div style="display:flex; justify-content:space-between; padding-top:6px; font-weight:700; font-size:13px; color:#111; border-top:1.5px solid #111; margin-top:6px;">
              <span>Grand Total Paid:</span>
              <span>$${inv.financials.total_usd.toFixed(2)} <span style="color:#166534;">(${inv.financials.formatted_inr})</span></span>
            </div>
          `;
        }

        if (billPrompt) billPrompt.style.display = 'none';
        if (billCard) billCard.style.display = 'block';
        showToast('Official Bill generated on request.');
      } catch (err) {
        renderLocalBill(orderId, orderDetails);
        if (billPrompt) billPrompt.style.display = 'none';
        if (billCard) billCard.style.display = 'block';
      } finally {
        if (triggerBtn) {
          triggerBtn.disabled = false;
          triggerBtn.innerHTML = '<span>⚡ Generate Bill & Tax Invoice</span>';
        }
      }
    }

    function renderLocalBill(orderId, orderDetails) {
      const invNumEl = document.getElementById('bill-inv-number');
      const invDateEl = document.getElementById('bill-inv-date');
      const billItemsList = document.getElementById('bill-items-list');
      const billTotalsSummary = document.getElementById('bill-totals-summary');

      if (invNumEl) invNumEl.textContent = `INV-2026-${orderId}`;
      if (invDateEl) invDateEl.textContent = new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });

      const items = (orderDetails && orderDetails.items) || [];
      const total = (orderDetails && orderDetails.total) || 0;
      const totalInr = total * 86.50;
      const formattedInr = '₹' + totalInr.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      const taxInr = (totalInr * 0.18 / 1.18);

      if (billItemsList) {
        billItemsList.innerHTML = items.map((itm) => `
          <div style="display: flex; justify-content: space-between; margin-bottom: 6px; padding-bottom: 6px; border-bottom: 1px dashed #eee;">
            <div>
              <strong style="color: #111;">${itm.title || 'Piece'}</strong>
              <div style="font-size: 11px; color: #777;">Size: ${itm.size || 'M'} · Qty: ${itm.quantity || 1}</div>
            </div>
            <div style="text-align: right; font-weight: 600; color: #111;">
              ${usd.format((Number(itm.price) || 0) * (Number(itm.quantity) || 1))}
              <div style="font-size: 10px; color: #166534;">₹${((Number(itm.price) || 0) * (Number(itm.quantity) || 1) * 86.50).toLocaleString('en-IN', { minimumFractionDigits: 2 })}</div>
            </div>
          </div>
        `).join('');
      }

      if (billTotalsSummary) {
        billTotalsSummary.innerHTML = `
          <div style="display:flex; justify-content:space-between; margin-bottom:4px; color:#666;">
            <span>Items Subtotal:</span>
            <span>${usd.format(total)}</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:4px; color:#666;">
            <span>GST (18% included):</span>
            <span>₹${taxInr.toFixed(2)}</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:4px; color:#666;">
            <span>Express Courier Delivery:</span>
            <span style="color:#166534; font-weight:600;">FREE</span>
          </div>
          <div style="display:flex; justify-content:space-between; padding-top:6px; font-weight:700; font-size:13px; color:#111; border-top:1.5px solid #111; margin-top:6px;">
            <span>Grand Total Paid:</span>
            <span>${usd.format(total)} <span style="color:#166534;">(${formattedInr})</span></span>
          </div>
        `;
      }
    }

    // Wiring trigger for on-demand generation
    const triggerGenerateBillBtn = document.getElementById('trigger-generate-bill-btn');
    if (triggerGenerateBillBtn) {
      triggerGenerateBillBtn.addEventListener('click', () => {
        if (!lastConfirmedOrder) return;
        generateBillOnDemand(lastConfirmedOrder.id, lastConfirmedOrder);
      });
    }

    // Bill Action Buttons Wiring (Print & Download)
    const viewBillBtn = document.getElementById('view-bill-btn');
    const downloadBillBtn = document.getElementById('download-bill-btn');

    if (viewBillBtn) {
      viewBillBtn.addEventListener('click', () => {
        if (!lastConfirmedOrder) return;
        const invoiceUrl = `http://127.0.0.1:8001/api/orders/${lastConfirmedOrder.id}/invoice/html`;
        window.open(invoiceUrl, '_blank');
      });
    }

    if (downloadBillBtn) {
      downloadBillBtn.addEventListener('click', async () => {
        if (!lastConfirmedOrder) return;
        downloadBillBtn.textContent = 'Generating...';
        try {
          const res = await fetch(`http://127.0.0.1:8001/api/orders/${lastConfirmedOrder.id}/invoice/html`);
          const html = await res.text();
          const blob = new Blob([html], { type: 'text/html' });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `Tax-Invoice-${lastConfirmedOrder.id}.html`;
          document.body.appendChild(a);
          a.click();
          a.remove();
          URL.revokeObjectURL(url);
          showToast(`Invoice downloaded for Order ${lastConfirmedOrder.id}`);
        } catch (err) {
          window.open(`http://127.0.0.1:8001/api/orders/${lastConfirmedOrder.id}/invoice/html`, '_blank');
        } finally {
          downloadBillBtn.innerHTML = '<span>📥 Download (.html)</span>';
        }
      });
    }

    // Header Member Profile Popover & Signout Wiring
    const headerAccountBtn = document.getElementById('header-account-btn');
    const memberPopover = document.getElementById('member-profile-popover');
    const popoverAvatar = document.getElementById('popover-avatar');
    const popoverName = document.getElementById('popover-name');
    const popoverEmail = document.getElementById('popover-email');
    const popoverCartBadge = document.getElementById('popover-cart-badge');
    const popoverCartBtn = document.getElementById('popover-cart-btn');
    const popoverSignoutBtn = document.getElementById('popover-signout-btn');
    const accountBadge = document.getElementById('account-active-badge');

    function syncUserHeader() {
      try {
        const raw = localStorage.getItem('atelier_user');
        if (raw) {
          const u = JSON.parse(raw);
          if (accountBadge) accountBadge.style.display = 'block';
          if (headerAccountBtn) headerAccountBtn.title = 'Logged in as ' + (u.name || 'Member');
          if (popoverName) popoverName.textContent = u.name || 'Member';
          if (popoverEmail) popoverEmail.textContent = u.email || 'member@atelier.com';
          if (popoverAvatar) popoverAvatar.textContent = (u.name || 'M').charAt(0).toUpperCase();
        } else {
          if (accountBadge) accountBadge.style.display = 'none';
          if (headerAccountBtn) headerAccountBtn.title = 'Account Login';
        }
      } catch (e) {}
    }
    syncUserHeader();

    if (headerAccountBtn && memberPopover) {
      headerAccountBtn.addEventListener('click', (e) => {
        const raw = localStorage.getItem('atelier_user');
        if (raw) {
          e.preventDefault();
          const isOpen = memberPopover.style.display === 'block';
          memberPopover.style.display = isOpen ? 'none' : 'block';
          if (popoverCartBadge) {
            popoverCartBadge.textContent = String(bagEntries.reduce((s, i) => s + (Number(i.quantity) || 1), 0));
          }
        }
      });

      document.addEventListener('click', (e) => {
        if (!e.target.closest('#header-account-btn') && !e.target.closest('#member-profile-popover')) {
          memberPopover.style.display = 'none';
        }
      });
    }

    if (popoverCartBtn && dialog) {
      popoverCartBtn.addEventListener('click', () => {
        if (memberPopover) memberPopover.style.display = 'none';
        resetDialogViews();
        renderBagDialog();
        dialog.showModal();
      });
    }

    if (popoverSignoutBtn) {
      popoverSignoutBtn.addEventListener('click', () => {
        localStorage.removeItem('atelier_user');
        localStorage.removeItem('atelier_token');
        if (memberPopover) memberPopover.style.display = 'none';
        if (accountBadge) accountBadge.style.display = 'none';
        if (headerAccountBtn) headerAccountBtn.title = 'Account Login';
        showToast('Signed out of Atelier Member account.');
      });
    }

    // Auto-open bag & trigger checkout if returning from login with ?checkout=true
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('checkout') === 'true' && dialog) {
      sessionStorage.removeItem('pending_checkout');
      setTimeout(() => {
        resetDialogViews();
        renderBagDialog();
        dialog.showModal();
        if (checkoutBtn && bagEntries.length > 0) {
          checkoutBtn.click();
        }
      }, 500);
    }
  }

    function clamp(v, lo, hi) {
    return v < lo ? lo : v > hi ? hi : v;
  }

  function wrapMod(v, n) {
    return ((v % n) + n) % n;
  }

  function decodeModelImage(img) {
    if (!img || img.classList.contains('is-decoded')) return;
    const mark = () => {
      img.classList.add('is-decoded');
    };
    if (typeof img.decode === 'function') {
      img.decode().then(mark, () => {
        if (img.naturalWidth > 0) mark();
      });
    }
    if (img.complete && img.naturalWidth > 0) {
      mark();
    } else {
      img.addEventListener('load', () => {
        if (typeof img.decode === 'function') {
          img.decode().then(mark, () => {
            if (img.naturalWidth > 0) mark();
          });
        } else {
          mark();
        }
      }, { once: true });
    }
  }

  class RunwaySection extends HTMLElement {
    connectedCallback() {
      this.classList.add('rw--js');
      if (window.Shopify && window.Shopify.designMode) {
        this.classList.add('rw--design');
      }

      this._stage = this.querySelector('[data-rw-stage]');
      this._actorsEl = this.querySelector('[data-rw-actors]');
      this._heroesEl = this.querySelector('[data-rw-heroes]');
      this._panel = this.querySelector('.rw__panel');
      this._live = this.querySelector('[data-rw-live]');
      this._piecesLabel = this.querySelector('[data-rw-pieces]');
      this._ticks = Array.from(this.querySelectorAll('[data-rw-tick]'));
      this._autoBtn = this.querySelector('[data-rw-auto]');
      this._lb = this.querySelector('[data-rw-lb]');
      this._lbStage = this.querySelector('[data-rw-lb-stage]');
      this._lbKicker = this.querySelector('[data-rw-lb-kicker]');
      this._lbName = this.querySelector('[data-rw-lb-name]');
      this._cursor = this.querySelector('[data-rw-cursor]');

      this._heroes = Array.from(this.querySelectorAll('[data-rw-hero]'));
      this._panels = Array.from(this.querySelectorAll('[data-rw-panel]'));
      this._lookCount = this._heroes.length;
      this._N = this._lookCount * Math.ceil(8 / this._lookCount);

      this._reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      this._finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

      if (!this._finePointer && this._cursor) {
        this._cursor.remove();
        this._cursor = null;
      } else if (this._finePointer && this._cursor) {
        this.classList.add('rw--cursor');
      }

      const originals = Array.from(this.querySelectorAll('[data-rw-model]'));
      for (let a = this._lookCount; a < this._N; a++) {
        const clone = originals[a % this._lookCount].cloneNode(true);
        clone.setAttribute('data-rw-clone', '');
        clone.setAttribute('data-index', String(a));
        const img = clone.querySelector('[data-model-image]');
        if (img) img.setAttribute('loading', 'lazy');
        this._actorsEl.appendChild(clone);
      }

      this._allModelEls = Array.from(this._actorsEl.querySelectorAll('[data-rw-model]'));
      this.querySelectorAll('[data-model-image]').forEach(decodeModelImage);

      const startOffset = this._reducedMotion ? 0 : 1.15;
      this._index = 0;
      this._target = 0;
      this._cur = -startOffset;
      this._vel = 0;
      this._still = false;
      this._playing = false;
      this._engaged = false;
      this._panelHover = false;
      this._zoomed = false;
      this._visible = true;
      this._dragging = false;
      this._suppressClickUntil = 0;
      this._rafId = 0;
      this._lastTime = 0;
      this._autoTimer = 0;
      this._lbCleanTimer = 0;
      this._resizeTimer = 0;
      this._wheelAcc = 0;
      this._wheelLockUntil = 0;
      this._sheetHost = null;
      this._sheetOwner = null;

      this._latchedVh = window.innerHeight;
      this._lastWinW = window.innerWidth;
      this._mode = null;
      this._isMobile = false;
      this._W = 0;
      this._H = 0;
      this._unit = 200;
      this._fs = 1;

      this._bodies = this._allModelEls.map((el, a) => ({
        el,
        lookIndex: a % this._lookCount,
        w: 0,
        x: a + startOffset,
        g: a + startOffset,
        v: 0,
        prevGoal: a,
        trip: false,
        from: 0,
        lastBlur: ''
      }));

      this._initCards();
      this._initFeetDetection();
      this._initCursor();
      this._bindEvents();

      this._setIndex(0, true);
      this._measure();

      if (this._reducedMotion) {
        this.classList.add('is-revealed');
      } else {
        this._revealIO = new IntersectionObserver(
          (entries) => {
            if (entries.some((e) => e.isIntersecting)) {
              this._revealIO.disconnect();
              this._revealIO = null;
              requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                  this.classList.add('is-revealed');
                  this._kick();
                });
              });
            }
          },
          { threshold: 0, rootMargin: '0px 0px -22% 0px' }
        );
        this._revealIO.observe(this);
      }

      this._visIO = new IntersectionObserver(
        (entries) => {
          this._visible = entries.some((e) => e.isIntersecting);
          if (this._visible) {
            this._kick();
            if (this._playing) this._restartAutoBar();
          }
        },
        { threshold: 0 }
      );
      this._visIO.observe(this);

      this._ro = new ResizeObserver(() => this._measure());
      if (this._stage) this._ro.observe(this._stage);

      if (
        this.dataset.autoplay === 'true' &&
        !this._reducedMotion &&
        !(window.Shopify && window.Shopify.designMode)
      ) {
        this._play(true);
      }

      this._kick();
    }

    disconnectedCallback() {
      if (this._rafId) cancelAnimationFrame(this._rafId);
      if (this._cursorRaf) cancelAnimationFrame(this._cursorRaf);
      clearTimeout(this._autoTimer);
      clearTimeout(this._lbCleanTimer);
      clearTimeout(this._resizeTimer);
      if (this._revealIO) this._revealIO.disconnect();
      if (this._visIO) this._visIO.disconnect();
      if (this._ro) this._ro.disconnect();
      window.removeEventListener('resize', this._onResize);
      document.removeEventListener('visibilitychange', this._onVisChange);
      document.removeEventListener('shopify:block:select', this._onBlockSelect);
      this._dockSheet(false);
    }

    _initCards() {
      this.querySelectorAll('.rw__item').forEach((card) => {
        const picker = card.querySelector('[data-rw-picker]');
        if (!picker) return;
        const jsonEl = picker.querySelector('[data-rw-variants]');
        if (jsonEl) {
          try {
            card._variants = JSON.parse(jsonEl.textContent || '[]');
          } catch {
            card._variants = [];
          }
        } else {
          card._variants = [];
        }
        this._updateOptions(picker, card, false);
      });
    }

    _initFeetDetection() {
      this._heroes.forEach((hero, i) => {
        const probeUrl = hero.dataset.probe;
        if (!probeUrl) return;
        const img = new Image();
        img.crossOrigin = 'anonymous';
        img.onload = () => {
          try {
            const w = 48;
            const h = Math.max(1, Math.round((w * img.naturalHeight) / (img.naturalWidth || 1)));
            const canvas = document.createElement('canvas');
            canvas.width = w;
            canvas.height = h;
            const ctx = canvas.getContext('2d');
            if (!ctx) return;
            ctx.drawImage(img, 0, 0, w, h);
            const data = ctx.getImageData(0, 0, w, h).data;
            let lastRow = h - 1;
            let found = false;
            for (let y = h - 1; y >= 0; y--) {
              for (let x = 0; x < w; x++) {
                if (data[(y * w + x) * 4 + 3] > 40) {
                  lastRow = y;
                  found = true;
                  break;
                }
              }
              if (found) break;
            }
            if (!found) return;
            const foot = clamp((h - 1 - lastRow) / h, 0, 0.4);
            const val = foot.toFixed(4);
            hero.style.setProperty('--rw-foot', val);
            this._bodies.forEach((b) => {
              if (b.lookIndex === i) b.el.style.setProperty('--rw-foot', val);
            });
          } catch {
            // Keep default 0 offset if canvas is tainted
          }
        };
        img.src = probeUrl;
      });
    }

    _initCursor() {
      if (!this._cursor || !this._stage) return;
      this._cx = 0;
      this._cy = 0;
      this._ctx = 0;
      this._cty = 0;
      this._cOn = false;
      this._cursorRaf = 0;

      const step = () => {
        const lerp = this._reducedMotion ? 1 : 0.18;
        this._cx += (this._ctx - this._cx) * lerp;
        this._cy += (this._cty - this._cy) * lerp;
        this._cursor.style.transform = `translate3d(${this._cx.toFixed(1)}px, ${this._cy.toFixed(1)}px, 0)`;
        if (
          Math.abs(this._ctx - this._cx) > 0.2 ||
          Math.abs(this._cty - this._cy) > 0.2
        ) {
          this._cursorRaf = requestAnimationFrame(step);
        } else {
          this._cx = this._ctx;
          this._cy = this._cty;
          this._cursor.style.transform = `translate3d(${this._cx.toFixed(1)}px, ${this._cy.toFixed(1)}px, 0)`;
          this._cursorRaf = 0;
        }
      };

      this._stage.addEventListener('pointermove', (e) => {
        if (e.pointerType !== 'mouse') return;
        const rect = this._stage.getBoundingClientRect();
        this._ctx = e.clientX - rect.left;
        this._cty = e.clientY - rect.top;
        if (!this._cOn) {
          this._cOn = true;
          this._cx = this._ctx;
          this._cy = this._cty;
          this._cursor.style.transform = `translate3d(${this._cx.toFixed(1)}px, ${this._cy.toFixed(1)}px, 0)`;
          this._cursor.classList.add('is-on');
        } else if (!this._cursorRaf) {
          this._cursorRaf = requestAnimationFrame(step);
        }

        const target = e.target;
        const isLink = !this._dragging && !!target.closest('.rw__pin, .rw__hit');
        const isView = !this._dragging && !isLink && !!target.closest('.rw__zoom');
        this._cursor.classList.toggle('is-link', isLink);
        this._cursor.classList.toggle('is-view', isView);
      });

      this._stage.addEventListener('pointerleave', () => {
        this._cOn = false;
        this._cursor.classList.remove('is-on', 'is-link', 'is-view');
      });
    }

    _bindEvents() {
      this._onResize = () => {
        clearTimeout(this._resizeTimer);
        this._resizeTimer = window.setTimeout(() => this._measure(), 120);
      };
      window.addEventListener('resize', this._onResize);

      this._onVisChange = () => {
        if (!document.hidden && this._visible) {
          this._kick();
          if (this._playing) this._restartAutoBar();
        }
      };
      document.addEventListener('visibilitychange', this._onVisChange);

      this._onBlockSelect = (e) => {
        const block = e.target;
        if (!block || !this.contains(block)) return;
        const panel = block.closest('[data-rw-panel]');
        if (panel) {
          this.go(Number(panel.dataset.rwPanel));
        }
      };
      document.addEventListener('shopify:block:select', this._onBlockSelect);

      // Panel hover pauses autoplay advance
      if (this._panel) {
        this._panel.addEventListener('pointerenter', (e) => {
          if (e.pointerType === 'mouse') this._panelHover = true;
        });
        this._panel.addEventListener('pointerleave', (e) => {
          if (e.pointerType === 'mouse') {
            this._panelHover = false;
            if (this._playing) this._restartAutoBar();
          }
        });

        this._panel.addEventListener('click', (e) => {
          if (e.target.closest('button, a, input, select, label')) {
            this._engage();
          }
        });
        this._panel.addEventListener('change', (e) => {
          this._engage();
          const input = e.target.closest('input[data-rw-option]');
          if (!input) return;
          const picker = input.closest('[data-rw-picker]');
          const card = input.closest('.rw__item');
          if (picker && card) this._updateOptions(picker, card, true);
        });

        this._panel.addEventListener('pointerover', (e) => {
          if (e.pointerType !== 'mouse') return;
          const card = e.target.closest('.rw__item');
          if (card) this._hot(card.dataset.rwCard, false);
        });
        this._panel.addEventListener('pointerout', (e) => {
          if (e.pointerType !== 'mouse') return;
          const card = e.target.closest('.rw__item');
          if (card && !card.contains(e.relatedTarget)) {
            this._clearHot();
          }
        });
      }

      // Keyboard on stage and Escape inside section
      if (this._stage) {
        this._stage.addEventListener('keydown', (e) => {
          if (e.key === 'ArrowRight') {
            e.preventDefault();
            this.next();
          } else if (e.key === 'ArrowLeft') {
            e.preventDefault();
            this.prev();
          }
        });

        // Trackpad horizontal wheel
        this._stage.addEventListener(
          'wheel',
          (e) => {
            if (Math.abs(e.deltaX) <= Math.abs(e.deltaY)) return;
            e.preventDefault();
            const now = performance.now();
            if (now < this._wheelLockUntil) return;
            this._wheelAcc += e.deltaX;
            if (Math.abs(this._wheelAcc) > 45) {
              if (this._wheelAcc > 0) this.next();
              else this.prev();
              this._wheelAcc = 0;
              this._wheelLockUntil = now + 520;
            }
          },
          { passive: false }
        );

        // Pointer drag / swipe
        let drag = null;

        this._stage.addEventListener('pointerdown', (e) => {
          if (e.pointerType === 'mouse' && e.button !== 0) return;
          if (e.target.closest('.rw__pin')) return;
          drag = {
            id: e.pointerId,
            type: e.pointerType,
            sx: e.clientX,
            sy: e.clientY,
            t0: this._target,
            active: false,
            samples: [{ x: e.clientX, time: performance.now() }]
          };
        });

        this._stage.addEventListener('pointermove', (e) => {
          if (!drag || e.pointerId !== drag.id) return;
          if (drag.type === 'mouse' && e.buttons === 0) {
            finishDrag(e);
            return;
          }
          const dx = e.clientX - drag.sx;
          const dy = e.clientY - drag.sy;
          if (!drag.active) {
            if (Math.abs(dy) > 10 && Math.abs(dy) >= Math.abs(dx)) {
              drag = null;
              return;
            }
            if (Math.abs(dx) > 8 && Math.abs(dx) > 1.2 * Math.abs(dy)) {
              drag.active = true;
              this._dragging = true;
              this.classList.add('is-dragging');
              this._setStill(false);
              try {
                this._stage.setPointerCapture(drag.id);
              } catch {
                // ignore
              }
            } else {
              return;
            }
          }

          drag.samples.push({ x: e.clientX, time: performance.now() });
          if (drag.samples.length > 6) drag.samples.shift();

          this._target = drag.t0 - dx / this._unit;
          if (this._reducedMotion) this._cur = this._target;
          this._kick();
        });

        const finishDrag = (e) => {
          if (!drag || e.pointerId !== drag.id) return;
          const d = drag;
          drag = null;
          if (!d.active) return;

          this._dragging = false;
          this.classList.remove('is-dragging');
          this._suppressClickUntil = performance.now() + 60;

          const dx = e.clientX - d.sx;
          const samples = d.samples;
          const first = samples[0];
          const last = samples[samples.length - 1];
          const dt = Math.max(1, last.time - first.time);
          const vx = (last.x - first.x) / dt;
          const sign = -1;
          const from = Math.round(d.t0);

          if (this._isMobile) {
            if (Math.abs(dx) > 30 || Math.abs(vx) > 0.3) {
              this._moveTo(from + sign * (dx > 0 ? 1 : -1));
            } else {
              this._moveTo(from);
            }
          } else {
            let i = Math.round(this._target + (sign * vx * 160) / this._unit);
            if (i === from && Math.abs(vx) > 0.3) {
              i = from + sign * (vx > 0 ? 1 : -1);
            }
            i = clamp(i, from - 2, from + 2);
            this._moveTo(i);
          }
        };

        this._stage.addEventListener('pointerup', finishDrag);
        this._stage.addEventListener('pointercancel', finishDrag);
      }

      this.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          if (this._sheetOwner) {
            this._dockSheet(true);
          } else if (this._zoomed) {
            this._closePopup();
          }
        }
      });

      // Capture-phase click suppressor after drag
      this.addEventListener(
        'click',
        (e) => {
          if (performance.now() < this._suppressClickUntil) {
            e.preventDefault();
            e.stopPropagation();
          }
        },
        true
      );

      // Delegated clicks inside section
      this.addEventListener('click', (e) => this._routeClick(e));
    }

    _routeClick(e) {
      const target = e.target;

      // 1. pick-close
      if (target.closest('[data-rw-pick-close]')) {
        if (this._sheetOwner) {
          this._dockSheet(true);
        } else {
          const card = target.closest('.rw__item');
          if (card) this._closeDesktopPicker(card);
        }
        return;
      }

      // 2. popup close button
      if (target.closest('[data-rw-zoom-close]')) {
        this._closePopup();
        return;
      }

      // 3. click on popup backdrop or stage beside the model
      if (this._zoomed && target.closest('[data-rw-lb]')) {
        if (!target.closest('.rw__lb-model') && !target.closest('.rw__lb-top')) {
          this._closePopup();
          return;
        }
      }

      // 4. zoom open
      if (target.closest('[data-rw-zoom]')) {
        this._openPopup();
        return;
      }

      // 5. next
      if (target.closest('[data-rw-next]')) {
        this.next();
        return;
      }

      // 6. prev
      if (target.closest('[data-rw-prev]')) {
        this.prev();
        return;
      }

      // 7. tick
      const tick = target.closest('[data-rw-tick]');
      if (tick) {
        this.go(Number(tick.dataset.rwTick));
        return;
      }

      // 8. autoplay toggle
      if (target.closest('[data-rw-auto]')) {
        if (!this._playing) {
          this._engaged = false;
          this._play(true);
        } else {
          this._play(false);
        }
        return;
      }

      // 9. pin
      const pin = target.closest('[data-rw-pin]');
      if (pin) {
        this._engage();
        this._hot(pin.dataset.rwPin, true);
        return;
      }

      // 10. queue body hit
      const goHit = target.closest('[data-rw-go]');
      if (goHit) {
        const bodyEl = goHit.closest('[data-rw-model]');
        const bodyIdx = bodyEl ? Number(bodyEl.dataset.index) : -1;
        const k = this._rankForBody(bodyIdx);
        if (k === 0) {
          this._openPopup();
        } else if (Math.abs(k) < this._lookCount) {
          this._moveTo(Math.round(this._target) + k);
        }
        return;
      }

      // 11. size confirm
      const confirmBtn = target.closest('[data-rw-confirm]');
      if (confirmBtn) {
        const card = this._cardForNode(confirmBtn);
        if (card) this._confirmCard(card);
        return;
      }

      // 12. plus button
      const addBtn = target.closest('[data-rw-add]');
      if (addBtn) {
        const card = addBtn.closest('.rw__item');
        if (card) this._togglePicker(card);
        return;
      }

      // 13. add full look
      const allBtn = target.closest('[data-rw-all]');
      if (allBtn) {
        this._addFullLook(allBtn);
      }
    }

    _cardForNode(node) {
      const inside = node.closest('.rw__item');
      if (inside) return inside;
      if (this._sheetOwner && this._sheetOwner.picker.contains(node)) {
        return this._sheetOwner.card;
      }
      return null;
    }

    _rankForBody(a) {
      if (a < 0) return 0;
      if (this._mode === 'ring') {
        const curLook = wrapMod(a - Math.round(this._target), this._N);
        return curLook > this._N / 2 ? curLook - this._N : curLook;
      }
      return wrapMod(a - Math.round(this._target), this._N);
    }

    _measure() {
      this._isMobile = window.innerWidth <= 749;
      const nextMode = this._isMobile
        ? this.dataset.mstyle || 'classic'
        : this.dataset.style || 'ring';

      if (this._mode && this._mode !== nextMode) {
        if (!this._isMobile && this._sheetOwner) {
          this._dockSheet(false);
        }
        this._cur = this._target;
        this._vel = 0;
        this._bodies.forEach((b, a) => {
          const g = wrapMod(a - this._target, this._N);
          b.x = g;
          b.g = g;
          b.v = 0;
          b.prevGoal = g;
          b.trip = false;
        });
      }
      this._mode = nextMode;

      let frameH;
      if (!this._isMobile) {
        let headerH = 0;
        document
          .querySelectorAll(
            '.shopify-section-group-header-group, #shopify-section-header, #shopify-section-announcement-bar'
          )
          .forEach((el) => {
            if (!el.contains(this) && el.offsetHeight > 0) {
              headerH += el.offsetHeight;
            }
          });
        frameH = Math.max(380, window.innerHeight - headerH);
      } else {
        if (
          window.innerWidth !== this._lastWinW ||
          Math.abs(window.innerHeight - this._latchedVh) >= 160
        ) {
          this._latchedVh = window.innerHeight;
          this._lastWinW = window.innerWidth;
        }
        const pct = clamp(Number(this.dataset.mheightVh || 109), 50, 120);
        frameH = Math.round((this._latchedVh * pct) / 100);
      }
      this.style.setProperty('--rw-frame-h', frameH + 'px');

      if (!this._stage) return;
      const rect = this._stage.getBoundingClientRect();
      this._W = rect.width;
      this._H = rect.height;

      this._fs = this._mode === 'ring' ? 1.08 : 1;
      this._stage.style.setProperty('--rw-fs', String(this._fs));

      let modelH;
      if (this._mode === 'ring') {
        modelH = Math.max(200, Math.round((this._H - 34 - 18) / 1.08));
      } else {
        const yOff = this._isMobile ? 24 : 36;
        modelH = Math.max(200, Math.round(this._H - yOff - 18));
      }
      this._stage.style.setProperty('--rw-model-h', modelH + 'px');

      let hx;
      let hy;
      if (this._mode === 'ring') {
        hx = 0.5 * this._W;
        hy = 34;
        this._unit = Math.max(this._isMobile ? 90 : 120, 0.3 * this._W);
      } else {
        hx = (this._isMobile ? 0.3 : 0.4) * this._W;
        hy = this._isMobile ? 22 : 36;
        const sx = this._isMobile ? 0.32 : 0.125;
        this._unit = Math.max(this._isMobile ? 90 : 120, this._W * sx * 1.6);
      }

      this._stage.style.setProperty('--rw-hx', hx + 'px');
      this._stage.style.setProperty('--rw-hy', hy + 'px');
      this.style.setProperty(
        '--rw-ax',
        (this._W > 0 ? ((hx / this._W) * 100).toFixed(2) : 40) + '%'
      );

      for (const b of this._bodies) {
        b.w = b.el.offsetWidth || Math.round(modelH * 0.5625);
      }

      if (this._zoomed && this._lbStage) {
        const wrap = this._lbStage.querySelector('.rw__lb-model');
        if (wrap) {
          const lbRect = this._lbStage.getBoundingClientRect();
          const h = Math.max(160, Math.min(lbRect.height, lbRect.width / 0.5625));
          wrap.style.setProperty('--rw-model-h', Math.round(h) + 'px');
          const img = wrap.querySelector('[data-model-image]');
          if (img) img.sizes = Math.round(h * 0.5625) + 'px';
        }
      }

      this._renderAll();
    }

    _setStill(val) {
      if (this._still === val) return;
      this._still = val;
      this.classList.toggle('rw--still', val);
    }

    _put(b, x, bottom, scale, opacity, blur, z) {
      const halfW = (b.w * scale) / 2;
      if (x + halfW < -4 || x - halfW > this._W + 4) {
        opacity = 0;
      }
      b.el.style.transform = `translate3d(${x.toFixed(2)}px, ${(-bottom).toFixed(2)}px, 0) translateX(-50%) scale(${scale.toFixed(4)})`;
      b.el.style.opacity = opacity.toFixed(3);
      b.el.style.zIndex = String(z);
      b.el.style.visibility = opacity < 0.01 ? 'hidden' : 'visible';
      b.el.style.pointerEvents = opacity < 0.5 ? 'none' : '';
      const br = blur <= 0.05 ? '' : `blur(${blur.toFixed(1)}px)`;
      if (b.lastBlur !== br) {
        b.lastBlur = br;
        b.el.style.filter = br;
      }
    }

    _renderAll() {
      const W = this._W;
      const H = this._H;
      if (W <= 0 || H <= 0) return;

      const useBlur = this.dataset.blur === 'true';

      if (this._mode === 'ring') {
        const cx = 0.5 * W;
        const R = (this._isMobile ? 0.72 : 0.62) * W;
        const P = (this._isMobile ? 1.9 : 1.65) * W;
        const floor = H - 34;
        const horizon = 0.36 * H;
        const step = (2 * Math.PI) / this._N;
        const TAU = 2 * Math.PI;

        for (let a = 0; a < this._N; a++) {
          const b = this._bodies[a];
          let phi = (((a - this._cur) * step) % TAU + TAU) % TAU;
          if (phi > Math.PI) phi -= TAU;
          const zDepth = R * (1 - Math.cos(phi));
          const persp = P / (P + zDepth);
          const sl = Math.abs(phi) / step;
          const scale = persp * (1 + (this._fs - 1) * clamp(1 - sl, 0, 1));
          const x = cx + R * Math.sin(phi) * persp;
          const feet = horizon + (floor - horizon) * persp;
          const bottom = H - feet;
          const blur = useBlur
            ? sl <= 1
              ? 1.8 * sl
              : Math.min(1.8 + (sl - 1) * 2, 6.5)
            : 0;
          let opacity = clamp((Math.cos(phi) + 0.55) / 0.3, 0, 1);
          if (this._still && sl < 0.02) opacity = 0;
          const z = Math.round(scale * 1000);
          this._put(b, x, bottom, scale, opacity, blur, z);
        }
      } else {
        const ax = this._isMobile ? 0.3 : 0.4;
        const ay = this._isMobile ? 22 : 36;
        const sx = this._isMobile ? 0.32 : 0.125;
        const sy = this._isMobile ? 22 : 58;
        const sr = 0.76;
        const ex = this._isMobile ? 0.55 : 0.38;
        const d = this._isMobile ? 4 : 5;

        for (let a = 0; a < this._N; a++) {
          const b = this._bodies[a];
          const xPlace = b.x;
          const goal = wrapMod(a - this._target, this._N);
          let k = xPlace;
          let e = -1;

          if (b.trip && Math.abs(goal - b.from) > 0.0001) {
            const u = clamp(
              Math.abs(xPlace - b.from) / Math.abs(goal - b.from),
              0,
              1
            );
            if (goal > b.from) {
              if (u < 0.5) e = 2 * u * 1.4;
              else k = goal + 2 * (1 - u);
            } else {
              if (u < 0.5) k = b.from + 2 * u;
              else e = 2 * (1 - u) * 1.4;
            }
          } else if (k < 0) {
            e = Math.min(-k, 1.4);
          }

          if (e >= 0) {
            const px = W * (ax - ex * e);
            const bottom = ay - 22 * e;
            const scale = 1 + 0.14 * e;
            const opacity = Math.max(0, 1 - 1.05 * e);
            const blur = useBlur ? 4 * Math.min(e, 1) : 0;
            this._put(b, px, bottom, scale, opacity, blur, 1100);
          } else {
            const px = W * (ax + sx * k);
            const bottom = ay + sy * k;
            const scale = Math.pow(sr, k);
            let opacity =
              k <= d - 1 ? 1 - 0.13 * k : Math.max(0, 0.61 * (d - k));
            if (this._still && Math.abs(k) < 0.02) opacity = 0;
            const blur = useBlur ? Math.min(0.9 * k, 3.2) : 0;
            const z = 1000 - Math.round(10 * k);
            this._put(b, px, bottom, scale, opacity, blur, z);
          }
        }
      }
    }

    _kick() {
      if (this._rafId || !this._visible || document.hidden) return;
      this._lastTime = 0;
      this._rafId = requestAnimationFrame((t) => this._loop(t));
    }

    _loop(now) {
      if (!this._visible || document.hidden) {
        this._rafId = 0;
        this._lastTime = 0;
        return;
      }

      const dt = this._lastTime
        ? Math.min(0.034, (now - this._lastTime) / 1000)
        : 1 / 60;
      this._lastTime = now;

      const K = 95;
      const C = 2 * Math.sqrt(K);
      let moving = false;

      if (this._reducedMotion) {
        this._cur = this._target;
        this._vel = 0;
        this._bodies.forEach((b, a) => {
          const g = wrapMod(a - this._target, this._N);
          b.x = g;
          b.g = g;
          b.v = 0;
          b.prevGoal = g;
          b.trip = false;
        });
      } else if (this._mode === 'ring') {
        const h = dt / 3;
        for (let s = 0; s < 3; s++) {
          const acc = -K * (this._cur - this._target) - C * this._vel;
          this._vel += acc * h;
          this._cur += this._vel * h;
        }
        if (
          !this._dragging &&
          Math.abs(this._cur - this._target) <= 0.0005 &&
          Math.abs(this._vel) <= 0.0005
        ) {
          this._cur = this._target;
          this._vel = 0;
        } else {
          moving = true;
        }
      } else {
        for (let a = 0; a < this._N; a++) {
          const b = this._bodies[a];
          const goal = wrapMod(a - this._target, this._N);
          if (Math.abs(goal - b.prevGoal) > this._N / 2) {
            b.trip = true;
            b.from = b.x;
          }
          b.prevGoal = goal;

          const tau = this._dragging
            ? 0.016
            : b.trip
            ? 0.1
            : 0.03 + 0.04 * Math.min(goal, 4);
          b.g += (goal - b.g) * (1 - Math.exp(-dt / tau));

          const h = dt / 3;
          for (let s = 0; s < 3; s++) {
            const acc = -K * (b.x - b.g) - C * b.v;
            b.v += acc * h;
            b.x += b.v * h;
          }

          if (b.trip && Math.abs(b.x - goal) < 0.02) {
            b.trip = false;
          }

          if (
            this._dragging ||
            b.trip ||
            Math.abs(b.x - goal) > 0.0006 ||
            Math.abs(b.g - goal) > 0.0006 ||
            Math.abs(b.v) > 0.0006
          ) {
            moving = true;
          } else {
            b.x = goal;
            b.g = goal;
            b.v = 0;
          }
        }
      }

      if (moving) {
        this._setStill(false);
        this._renderAll();
        this._rafId = requestAnimationFrame((t) => this._loop(t));
      } else {
        this._setStill(!this._dragging);
        this._renderAll();
        this._rafId = 0;
        this._lastTime = 0;
      }
    }

    _moveTo(T) {
      this._target = T;
      this._setStill(false);
      this._setIndex(wrapMod(T, this._lookCount), false);
      this._kick();
    }

    next() {
      this._moveTo(Math.round(this._target) + 1);
    }

    prev() {
      this._moveTo(Math.round(this._target) - 1);
    }

    go(i) {
      let d = wrapMod(i - this._index, this._lookCount);
      if (d > this._lookCount / 2) d -= this._lookCount;
      this._moveTo(Math.round(this._target) + d);
    }

    _setIndex(i, silent) {
      const prev = this._index;
      this._index = i;
      this._kick();

      // Accessibility of queue bodies
      const maxK = this._mode === 'ring' ? 2 : 3;
      this._bodies.forEach((b, a) => {
        const k = this._rankForBody(a);
        const hit = b.el.querySelector('.rw__hit');
        const interactive = k !== 0 && Math.abs(k) <= maxK;
        if (interactive) {
          b.el.removeAttribute('aria-hidden');
          if (hit) hit.tabIndex = 0;
        } else {
          b.el.setAttribute('aria-hidden', 'true');
          if (hit) hit.tabIndex = -1;
        }
      });

      this.style.setProperty(
        '--rw-progress',
        ((i + 1) / this._lookCount).toFixed(3)
      );

      if (silent) return;

      if (this._zoomed) this._closePopup();
      if (this._sheetOwner) this._dockSheet(false);

      this._heroes.forEach((h, idx) => {
        h.classList.remove('was', 'is-on');
        if (idx === prev && idx !== i) h.classList.add('was');
        if (idx === i) {
          h.classList.add('is-on');
          h.removeAttribute('aria-hidden');
        } else {
          h.setAttribute('aria-hidden', 'true');
        }
        const zoomBtn = h.querySelector('[data-rw-zoom]');
        if (zoomBtn) zoomBtn.tabIndex = idx === i ? 0 : -1;
      });

      if (!this._reducedMotion && this._stage) {
        this._stage.classList.remove('is-sweep');
        void this._stage.offsetWidth;
        this._stage.classList.add('is-sweep');
      }

      const activeHero = this._heroes[i];
      if (this._live && activeHero) {
        this._live.textContent = activeHero.dataset.label || '';
      }

      this._ticks.forEach((t, idx) => {
        t.setAttribute('aria-current', idx === i ? 'true' : 'false');
        t.classList.toggle('is-past', idx < i);
      });

      this._panels.forEach((p, idx) => {
        p.classList.remove('is-in');
        p.hidden = idx !== i;
      });
      const activePanel = this._panels[i];
      if (activePanel) {
        void activePanel.offsetWidth;
        activePanel.classList.add('is-in');
        const tpl = activePanel.querySelector('[data-rw-pieces-text]');
        if (this._piecesLabel && tpl) {
          this._piecesLabel.textContent = tpl.content.textContent.trim();
          this._piecesLabel.classList.remove('is-swap');
          void this._piecesLabel.offsetWidth;
          this._piecesLabel.classList.add('is-swap');
        }
      }

      this._clearHot();
      if (this._playing) this._restartAutoBar();
    }

    _play(on) {
      this._playing = on;
      this.classList.toggle('is-playing', on);
      if (this._autoBtn) {
        this._autoBtn.classList.toggle('is-playing', on);
        this._autoBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
      }
      if (on) {
        this._restartAutoBar();
      } else {
        clearTimeout(this._autoTimer);
        this._ticks.forEach((t) => t.classList.remove('is-run'));
      }
    }

    _restartAutoBar() {
      clearTimeout(this._autoTimer);
      this._ticks.forEach((t) => t.classList.remove('is-run'));
      const currentTick = this._ticks[this._index];
      if (currentTick) {
        void currentTick.offsetWidth;
        currentTick.classList.add('is-run');
      }
      const speed = Math.max(1000, Number(this.dataset.speed || 5000));
      this._autoTimer = window.setTimeout(() => {
        if (!this._playing) return;
        if (
          this._visible &&
          !this._dragging &&
          !document.hidden &&
          !this._panelHover &&
          !this._zoomed &&
          !this._engaged
        ) {
          this.next();
        } else {
          this._restartAutoBar();
        }
      }, speed);
    }

    _engage() {
      if (this._engaged) return;
      this._engaged = true;
      if (this._playing) this._play(false);
    }

    _clearHot() {
      this.querySelectorAll('.is-hot').forEach((el) => el.classList.remove('is-hot'));
    }

    _hot(n, scroll) {
      this._clearHot();
      const num = String(n);
      const pinContainer = this._zoomed ? this._lbStage : this._heroes[this._index];
      if (pinContainer) {
        const pin = pinContainer.querySelector(`[data-rw-pin="${num}"]`);
        if (pin) pin.classList.add('is-hot');
      }
      const panel = this._panels[this._index];
      if (!panel) return;
      const card = panel.querySelector(`[data-rw-card="${num}"]`);
      if (!card) return;
      card.classList.add('is-hot');

      if (!scroll) return;
      const list = panel.querySelector('.rw__items');
      const behavior = this._reducedMotion ? 'auto' : 'smooth';
      if (list) {
        if (list.scrollWidth > list.clientWidth + 2) {
          const left = card.getBoundingClientRect().left - list.getBoundingClientRect().left + list.scrollLeft - 20;
          list.scrollTo({ left, behavior });
        } else if (list.scrollHeight > list.clientHeight + 2) {
          list.scrollTo({ top: card.offsetTop - list.offsetTop - 12, behavior });
        } else {
          const r = card.getBoundingClientRect();
          if (r.top < 0 || r.bottom > window.innerHeight - 140) {
            window.scrollBy({ top: r.top - 0.3 * window.innerHeight, behavior });
          }
        }
      }
    }

    _openPopup() {
      this._engage();
      this._clearHot();
      clearTimeout(this._lbCleanTimer);

      const hero = this._heroes[this._index];
      if (!hero || !this._lb || !this._lbStage) return;

      const runwayFig = hero.querySelector('.rw__figure');
      const a = runwayFig ? runwayFig.getBoundingClientRect() : null;

      const wrap = document.createElement('div');
      wrap.className = 'rw__lb-model';

      const shadow = hero.querySelector('.rw__shadow');
      const figure = hero.querySelector('.rw__figure');
      if (shadow) wrap.appendChild(shadow.cloneNode(true));
      if (figure) {
        const figClone = figure.cloneNode(true);
        const zoomBtn = figClone.querySelector('[data-rw-zoom]');
        if (zoomBtn) zoomBtn.remove();
        figClone.querySelectorAll('[data-rw-pin]').forEach((pin) => {
          pin.tabIndex = 0;
        });
        const img = figClone.querySelector('[data-model-image]');
        if (img) {
          img.setAttribute('loading', 'eager');
          decodeModelImage(img);
        }
        const footVal = hero.style.getPropertyValue('--rw-foot');
        const art = figClone.querySelector('.rw__art');
        if (footVal && art) art.style.setProperty('--rw-foot', footVal);
        wrap.appendChild(figClone);
      }

      const lbRect = this._lbStage.getBoundingClientRect();
      const h = Math.max(160, Math.min(lbRect.height, lbRect.width / 0.5625));
      wrap.style.setProperty('--rw-model-h', Math.round(h) + 'px');
      const cloneImg = wrap.querySelector('[data-model-image]');
      if (cloneImg) cloneImg.sizes = Math.round(h * 0.5625) + 'px';

      this._lbStage.textContent = '';
      this._lbStage.appendChild(wrap);

      const word = this._lb.dataset.word || 'Look';
      if (this._lbKicker) {
        this._lbKicker.textContent = `${word} 0${this._index + 1}`;
      }
      if (this._lbName) {
        this._lbName.textContent = hero.dataset.name || '';
      }

      this.classList.add('rw--zoom');
      this._lb.setAttribute('aria-hidden', 'false');
      this._zoomed = true;

      if (!this._reducedMotion && a && a.height > 0) {
        const cloneFig = wrap.querySelector('.rw__figure');
        const b = cloneFig ? cloneFig.getBoundingClientRect() : null;
        if (b && b.height > 0) {
          wrap.style.transition = 'none';
          wrap.style.transformOrigin = '0 100%';
          wrap.style.transform = `translate3d(${a.left - b.left}px, ${a.bottom - b.bottom}px, 0) scale(${a.height / b.height})`;
          void wrap.offsetWidth;
          wrap.style.transition = '';
          wrap.style.transform = '';
        }
      }

      const closeBtn = this._lb.querySelector('[data-rw-zoom-close]');
      if (closeBtn) closeBtn.focus({ preventScroll: true });
    }

    _closePopup() {
      if (!this._zoomed || !this._lb || !this._lbStage) return;
      this._zoomed = false;
      const wasFocusInside = this._lb.contains(document.activeElement);

      const wrap = this._lbStage.querySelector('.rw__lb-model');
      if (!this._reducedMotion && wrap) {
        const hero = this._heroes[this._index];
        const runwayFig = hero ? hero.querySelector('.rw__figure') : null;
        const cloneFig = wrap.querySelector('.rw__figure');
        if (runwayFig && cloneFig) {
          const a = runwayFig.getBoundingClientRect();
          const b = cloneFig.getBoundingClientRect();
          if (a.height > 0 && b.height > 0) {
            wrap.style.transformOrigin = '0 100%';
            wrap.style.transform = `translate3d(${a.left - b.left}px, ${a.bottom - b.bottom}px, 0) scale(${a.height / b.height})`;
          }
        }
      }

      this.classList.remove('rw--zoom');
      this._lb.setAttribute('aria-hidden', 'true');
      this._clearHot();

      if (wasFocusInside && this._stage) {
        this._stage.focus({ preventScroll: true });
      }

      clearTimeout(this._lbCleanTimer);
      this._lbCleanTimer = window.setTimeout(
        () => {
          if (!this._zoomed && this._lbStage) {
            this._lbStage.textContent = '';
          }
        },
        this._reducedMotion ? 0 : 950
      );
    }

    _togglePicker(card) {
      if (card.classList.contains('is-added') || card.classList.contains('is-loading')) {
        return;
      }
      if (this._isMobile) {
        if (this._sheetOwner && this._sheetOwner.card === card) {
          this._dockSheet(true);
        } else {
          this._openSheet(card);
        }
      } else {
        const picker = card.querySelector('[data-rw-picker]');
        if (!picker) return;
        if (picker.hidden) {
          this._openDesktopPicker(card, true);
        } else {
          this._closeDesktopPicker(card);
        }
      }
    }

    _openDesktopPicker(card, focusRadio) {
      const picker = card.querySelector('[data-rw-picker]');
      const addBtn = card.querySelector('[data-rw-add]');
      if (!picker || !addBtn) return;
      picker.hidden = false;
      card.classList.add('is-picking');
      addBtn.setAttribute('aria-expanded', 'true');
      if (focusRadio) {
        const checked = picker.querySelector('input[type="radio"]:checked') || picker.querySelector('input[type="radio"]');
        if (checked) checked.focus({ preventScroll: true });
      }
    }

    _closeDesktopPicker(card) {
      const picker = card.querySelector('[data-rw-picker]');
      const addBtn = card.querySelector('[data-rw-add]');
      if (!picker || !addBtn) return;
      picker.hidden = true;
      card.classList.remove('is-picking');
      addBtn.setAttribute('aria-expanded', 'false');
    }

    _openSheet(card) {
      if (this._sheetOwner) this._dockSheet(false);
      const picker = card.querySelector('[data-rw-picker]');
      const addBtn = card.querySelector('[data-rw-add]');
      if (!picker || !addBtn) return;

      const host = document.createElement('div');
      host.className = 'rw-sheet-host';

      const cs = getComputedStyle(this);
      const vars = [
        '--rw-panel',
        '--rw-text',
        '--rw-muted',
        '--rw-line',
        '--rw-accent',
        '--rw-on-accent',
        '--rw-btn-bg',
        '--rw-btn-fg',
        '--rw-btn-radius',
        '--rw-pill-radius',
        '--rw-bar-r',
        '--rw-thumb-radius',
        '--rw-pt-size',
        '--rw-price',
        '--rw-opt',
        '--rw-ease',
        '--rw-ease-sheet',
        '--rw-ease-spring'
      ];
      for (const v of vars) {
        host.style.setProperty(v, cs.getPropertyValue(v));
      }
      host.style.fontFamily = cs.fontFamily;
      host.style.color = cs.color;

      const scrim = document.createElement('button');
      scrim.type = 'button';
      scrim.className = 'rw__pick-scrim';
      scrim.setAttribute('data-rw-pick-close', '');
      scrim.tabIndex = -1;
      scrim.setAttribute('aria-hidden', 'true');

      host.appendChild(scrim);
      picker.hidden = false;
      host.appendChild(picker);
      document.body.appendChild(host);

      card.classList.add('is-picking');
      addBtn.setAttribute('aria-expanded', 'true');
      this.classList.add('rw--picking');

      this._sheetHost = host;
      this._sheetOwner = { card, picker, addBtn };

      host.addEventListener('click', (e) => {
        if (e.target.closest('[data-rw-pick-close]')) {
          this._dockSheet(true);
        } else if (e.target.closest('[data-rw-confirm]')) {
          this._confirmCard(card);
        }
      });

      host.addEventListener('change', (e) => {
        this._engage();
        const input = e.target.closest('input[data-rw-option]');
        if (input) this._updateOptions(picker, card, true);
      });

      host.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          e.stopPropagation();
          this._dockSheet(true);
        }
      });

      requestAnimationFrame(() => {
        host.classList.add('is-open');
      });

      const checked =
        picker.querySelector('input[type="radio"]:checked') ||
        picker.querySelector('[data-rw-pick-close]');
      if (checked) checked.focus({ preventScroll: true });
    }

    _dockSheet(returnFocus) {
      if (!this._sheetOwner) return;
      const { card, picker, addBtn } = this._sheetOwner;
      picker.hidden = true;
      card.appendChild(picker);
      card.classList.remove('is-picking');
      addBtn.setAttribute('aria-expanded', 'false');
      this.classList.remove('rw--picking');
      if (this._sheetHost) {
        this._sheetHost.remove();
        this._sheetHost = null;
      }
      this._sheetOwner = null;
      if (returnFocus) addBtn.focus({ preventScroll: true });
    }

    _updateOptions(picker, card, markTouched) {
      const variants = card._variants || [];
      const radios = Array.from(picker.querySelectorAll('input[data-rw-option]'));
      const selected = [];
      radios.forEach((r) => {
        const idx = Number(r.dataset.rwOption);
        if (r.checked) selected[idx] = r.value;
      });

      const match = variants.find((v) =>
        selected.every((val, idx) => val === undefined || v.o[idx] === val)
      );

      radios.forEach((r) => {
        const idx = Number(r.dataset.rwOption);
        const pill = r.closest('.rw__pill');
        if (!pill) return;
        const ok = variants.some(
          (v) =>
            v.a &&
            v.o[idx] === r.value &&
            selected.every((val, i) => i === idx || val === undefined || v.o[i] === val)
        );
        pill.classList.toggle('is-unavailable', !ok);
      });

      const confirmBtn = picker.querySelector('[data-rw-confirm]');
      const labelEl = picker.querySelector('[data-rw-confirm-label]');
      const isAvailable = !!(match && match.a);

      if (confirmBtn) confirmBtn.disabled = !isAvailable;
      if (labelEl) {
        labelEl.textContent = isAvailable
          ? labelEl.dataset.add || 'Add to bag'
          : this.dataset.msgSoldout || 'Sold out';
      }

      if (isAvailable) {
        card.dataset.selected = String(match.id);
      } else {
        delete card.dataset.selected;
      }

      if (markTouched) {
        card.dataset.touched = '1';
      }
    }

    _markAdded(card) {
      card.classList.remove('is-loading', 'is-picking');
      card.classList.add('is-added');
      const addBtn = card.querySelector('[data-rw-add]');
      if (addBtn) {
        addBtn.setAttribute('aria-label', addBtn.dataset.addedLabel || 'Added to bag');
        addBtn.removeAttribute('aria-expanded');
      }
      if (this._sheetOwner && this._sheetOwner.card === card) {
        this._dockSheet(false);
      } else {
        const picker = card.querySelector('[data-rw-picker]');
        if (picker) picker.hidden = true;
      }
    }

    _checkComplete(panel) {
      if (!panel) return;
      const cards = Array.from(panel.querySelectorAll('.rw__item'));
      if (cards.length >= 2 && cards.every((c) => c.classList.contains('is-added'))) {
        panel.classList.add('is-complete');
        const msg = panel.querySelector('[data-rw-msg]');
        if (msg) msg.textContent = '';
      }
    }

    _confirmCard(card) {
      this._engage();
      card.dataset.touched = '1';
      if (card.classList.contains('is-added') || card.classList.contains('is-loading')) {
        return;
      }
      const id = Number(card.dataset.selected);
      if (!id) return;

      const panel = card.closest('[data-rw-panel]');
      const msg = panel ? panel.querySelector('[data-rw-msg]') : null;
      if (msg) msg.textContent = '';

      card.classList.add('is-loading');

      window.setTimeout(() => {
        try {
          RunwayBag.add([{ id, quantity: 1 }]);
          this._markAdded(card);
          if (this._isMobile && !this._reducedMotion && navigator.vibrate) {
            navigator.vibrate(12);
          }
          this._checkComplete(panel);
        } catch {
          card.classList.remove('is-loading');
          if (msg) {
            msg.textContent = this.dataset.msgError || 'Couldn’t add to bag. Please try again.';
          }
        }
      }, 140);
    }

    _addFullLook(ctaBtn) {
      this._engage();
      const panel = ctaBtn.closest('[data-rw-panel]');
      if (!panel || panel.classList.contains('is-complete') || ctaBtn.classList.contains('is-loading')) {
        return;
      }

      const msg = panel.querySelector('[data-rw-msg]');
      if (msg) msg.textContent = '';

      const cards = Array.from(panel.querySelectorAll('.rw__item')).filter((c) => {
        if (c.classList.contains('is-added')) return false;
        const confirmBtn = c.querySelector('[data-rw-confirm]');
        if (confirmBtn && confirmBtn.disabled) return false;
        return true;
      });

      const ready = [];
      const pending = [];

      for (const c of cards) {
        if (c.dataset.variantId || (c.dataset.touched === '1' && c.dataset.selected)) {
          ready.push(c);
        } else {
          pending.push(c);
        }
      }

      const showPending = () => {
        if (pending.length === 0) return;
        if (this._isMobile) {
          this._openSheet(pending[0]);
        } else {
          pending.forEach((c) => this._openDesktopPicker(c, false));
        }
        const list = panel.querySelector('.rw__items');
        const behavior = this._reducedMotion ? 'auto' : 'smooth';
        if (list) {
          if (list.scrollWidth > list.clientWidth + 2) {
            const left =
              pending[0].getBoundingClientRect().left -
              list.getBoundingClientRect().left +
              list.scrollLeft -
              20;
            list.scrollTo({ left, behavior });
          } else if (list.scrollHeight > list.clientHeight + 2) {
            list.scrollTo({ top: pending[0].offsetTop - list.offsetTop - 12, behavior });
          }
        }
        if (msg) {
          const tpl = this.dataset.msgChoose || 'Pick a size for: [items]';
          msg.textContent = tpl.replace(
            '[items]',
            pending.map((c) => c.dataset.title || '').join(', ')
          );
        }
      };

      if (ready.length > 0) {
        ctaBtn.classList.add('is-loading');
        ready.forEach((c) => c.classList.add('is-loading'));
        window.setTimeout(() => {
          try {
            const payload = ready.map((c) => ({
              id: Number(c.dataset.variantId || c.dataset.selected),
              quantity: 1
            }));
            RunwayBag.add(payload);
            ready.forEach((c) => this._markAdded(c));
            ctaBtn.classList.remove('is-loading');
            if (this._isMobile && !this._reducedMotion && navigator.vibrate) {
              navigator.vibrate(12);
            }
            this._checkComplete(panel);
            showPending();
          } catch {
            ctaBtn.classList.remove('is-loading');
            ready.forEach((c) => c.classList.remove('is-loading'));
            if (msg) {
              msg.textContent = this.dataset.msgError || 'Couldn’t add to bag. Please try again.';
            }
          }
        }, 160);
      } else {
        showPending();
      }
    }
  }

  customElements.define('runway-section', RunwaySection);
  initBagUI();
})();
