/**
 * NIKEY STOREFRONT INTERACTIVE LOGIC
 * - Hand Rail Pro (Screens 1 & 2)
 * - Nike Orbit 3D Trajectory & Jog Wheel (Screen 3)
 */
(function () {
  'use strict';

  // --------------------------------------------------------------------------
  // 1. SNEAKERS DATA & 3D SPLINE PHYSICS ENGINE (NIKE ORBIT)
  // --------------------------------------------------------------------------
  const SNEAKERS = [
    {
      id: 'luka-5',
      name: 'LUKA 5',
      price: '$149.00',
      numericPrice: 149,
      image: '/assets/sneakers/sneaker-1.webp'
    },
    {
      id: 'tatum-5-orbit',
      name: 'TATUM 5 ORBIT',
      price: '$149.00',
      numericPrice: 149,
      image: '/assets/sneakers/sneaker-2.webp'
    },
    {
      id: 'air-jordan-12-retro',
      name: 'AIR JORDAN 12 RETRO',
      price: '$149.00',
      numericPrice: 149,
      image: '/assets/sneakers/sneaker-3.webp'
    },
    {
      id: 'air-jordan-1-retro',
      name: 'AIR JORDAN 1 RETRO',
      price: '$180.00',
      numericPrice: 180,
      image: '/assets/sneakers/sneaker-4.webp'
    },
    {
      id: 'air-jordan-3-cement',
      name: 'AIR JORDAN 3 CEMENT',
      price: '$210.00',
      numericPrice: 210,
      image: '/assets/sneakers/sneaker-5.webp'
    },
    {
      id: 'nike-dunk-low',
      name: 'NIKE DUNK LOW RETRO',
      price: '$115.00',
      numericPrice: 115,
      image: '/assets/sneakers/sneaker-6.webp'
    },
    {
      id: 'air-max-95-og',
      name: 'AIR MAX 95 OG',
      price: '$175.00',
      numericPrice: 175,
      image: '/assets/sneakers/sneaker-7.webp'
    }
  ];

  // 3D Spline Arc Nodes along Diagonal-Curved Depth Trajectory
  // Sweeping from bottom-center/left foreground (u = -1) up through Hero peak (u = 0)
  // and receding into 3D background space toward top-right (u = 1..3.5)
  // Both endpoints (u = -3.5 and u = +3.5) fade to opacity: 0.0 for 100% invisible wrap-around
  const SPLINE_NODES = [
    { u: -3.5, x: -0.06, y: 1.10, scale: 0.22, opacity: 0.0, rot: 22, z: 29 },
    { u: -2.5, x: 0.02,  y: 0.90, scale: 0.35, opacity: 0.0, rot: 18, z: 28 },
    { u: -1.0, x: 0.16,  y: 0.65, scale: 0.58, opacity: 0.65, rot: 12, z: 25 },
    { u: 0.0,  x: 0.32,  y: 0.36, scale: 1.0,  opacity: 1.0,  rot: -8, z: 22 },
    { u: 1.0,  x: 0.52,  y: 0.25, scale: 0.68, opacity: 0.85, rot: -14, z: 18 },
    { u: 2.0,  x: 0.67,  y: 0.19, scale: 0.48, opacity: 0.65, rot: -18, z: 14 },
    { u: 2.8,  x: 0.78,  y: 0.16, scale: 0.34, opacity: 0.45, rot: -22, z: 10 },
    { u: 3.5,  x: 0.90,  y: 0.15, scale: 0.20, opacity: 0.0,  rot: -26, z: 6 }
  ];

  function evaluateSpline(u, width, height) {
    if (u <= SPLINE_NODES[0].u) {
      const n = SPLINE_NODES[0];
      return { x: n.x * width, y: n.y * height, scale: n.scale, opacity: 0, rot: n.rot, z: n.z };
    }
    const lastNode = SPLINE_NODES[SPLINE_NODES.length - 1];
    if (u >= lastNode.u) {
      return { x: lastNode.x * width, y: lastNode.y * height, scale: lastNode.scale, opacity: 0, rot: lastNode.rot, z: lastNode.z };
    }

    for (let k = 0; k < SPLINE_NODES.length - 1; k++) {
      const n1 = SPLINE_NODES[k];
      const n2 = SPLINE_NODES[k + 1];
      if (u >= n1.u && u <= n2.u) {
        const rawT = (u - n1.u) / (n2.u - n1.u);
        // Smoothstep interpolation for C1 continuity
        const s = rawT * rawT * (3 - 2 * rawT);
        const lerp = (a, b, t) => a + (b - a) * t;

        return {
          x: lerp(n1.x, n2.x, s) * width,
          y: lerp(n1.y, n2.y, s) * height,
          scale: lerp(n1.scale, n2.scale, s),
          opacity: Math.max(0, Math.min(1, lerp(n1.opacity, n2.opacity, s))),
          rot: lerp(n1.rot, n2.rot, s),
          z: Math.round(lerp(n1.z, n2.z, rawT))
        };
      }
    }

    const mid = SPLINE_NODES[3];
    return { x: mid.x * width, y: mid.y * height, scale: mid.scale, opacity: mid.opacity, rot: mid.rot, z: mid.z };
  }

  function initOrbit() {
    const stage = document.getElementById('orbit-stage');
    const shoesGroup = document.getElementById('orbit-shoes-group');
    const shoeNodes = document.querySelectorAll('[data-orbit-shoe]');
    const metaInner = document.querySelector('.orbit-meta-inner');
    const nameEl = document.getElementById('orbit-name');
    const priceEl = document.getElementById('orbit-price');
    const counterEl = document.getElementById('orbit-counter');
    const dial = document.getElementById('orbit-dial');
    const ribs = document.getElementById('orbit-ribs');
    const indicator = document.getElementById('orbit-indicator');
    const thumbImg = document.getElementById('orbit-thumb-img');
    const indicatorTrack = document.querySelector('.orbit-jog-indicator-track');
    const sizeBtns = document.querySelectorAll('.orbit-size-btn');
    const addBtn = document.getElementById('orbit-add-bag');

    if (!stage || !shoeNodes.length) return;

    const N = SNEAKERS.length;
    let targetProgress = 0.0;
    let currentProgress = 0.0;
    let velocity = 0.0;
    let displayedIndex = -1;
    let selectedSize = '42';
    let isDragging = false;
    let dragStartX = 0;
    let dragStartProgress = 0;
    let lastDragX = 0;
    let lastDragTime = 0;
    let dragVelocity = 0;
    let wheelSnapTimer = null;

    // Cache shoe item node references
    const shoeItems = Array.from(shoeNodes).map((node, i) => ({
      el: node,
      img: node.querySelector('.orbit-shoe-img'),
      shadow: node.querySelector('.orbit-shoe-shadow'),
      index: i
    }));

    function updateProductMeta(idx) {
      if (idx === displayedIndex) return;
      displayedIndex = idx;
      const shoe = SNEAKERS[idx];
      if (!shoe) return;

      if (thumbImg) {
        thumbImg.src = shoe.image;
        thumbImg.alt = `${shoe.name} thumbnail`;
      }

      if (metaInner) {
        metaInner.classList.add('is-sliding-out');
        setTimeout(() => {
          if (counterEl) {
            counterEl.textContent = `${String(idx + 1).padStart(2, '0')} / 07`;
          }
          if (nameEl) nameEl.textContent = shoe.name;
          if (priceEl) priceEl.textContent = shoe.price;

          metaInner.classList.remove('is-sliding-out');
          metaInner.classList.add('is-sliding-in');
          requestAnimationFrame(() => {
            requestAnimationFrame(() => {
              metaInner.classList.remove('is-sliding-in');
            });
          });
        }, 150);
      }
    }

    // Size Selection
    sizeBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        sizeBtns.forEach((b) => b.classList.remove('is-selected'));
        btn.classList.add('is-selected');
        selectedSize = btn.dataset.size || btn.textContent.trim();
      });
    });

    // Add to Bag Button
    if (addBtn) {
      addBtn.addEventListener('click', () => {
        const shoe = SNEAKERS[displayedIndex] || SNEAKERS[0];
        if (window.AtelierCart) {
          window.AtelierCart.add({
            id: `orbit-${shoe.id}-${selectedSize}`,
            productId: shoe.id,
            name: shoe.name,
            price: shoe.numericPrice || 149,
            size: String(selectedSize || '42'),
            image: shoe.image,
            quantity: 1
          });
        } else {
          triggerBagToast(`${shoe.name} (Size ${selectedSize}) added to bag`);
          incrementCartCount();
        }
      });
    }

    // Click on any shoe along the arc to orbit it directly to hero focus (shortest arc)
    shoeItems.forEach((item) => {
      const handleClick = () => {
        const currentInt = Math.round(currentProgress);
        const rawDiff = ((item.index - currentInt) % N + N) % N;
        const diff = rawDiff > N / 2 ? rawDiff - N : rawDiff;
        targetProgress = currentInt + diff;
      };

      item.el.addEventListener('click', handleClick);
      item.el.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          handleClick();
        }
      });
    });

    // Scrubber & Stage Drag Handling
    function onPointerDown(clientX) {
      isDragging = true;
      dragStartX = clientX;
      lastDragX = clientX;
      lastDragTime = performance.now();
      dragStartProgress = currentProgress;
      dragVelocity = 0;
    }

    function onPointerMove(clientX, sensitivity = 320) {
      if (!isDragging) return;
      const now = performance.now();
      const dt = Math.max(1, now - lastDragTime);
      const dx = clientX - lastDragX;
      dragVelocity = (dx / dt) * 16.67; // normalized px per frame
      lastDragX = clientX;
      lastDragTime = now;

      // Delta relative to start - Infinite wrapping with NO clamping boundaries
      const totalDx = clientX - dragStartX;
      targetProgress = dragStartProgress - (totalDx / sensitivity);
    }

    function onPointerUp() {
      if (!isDragging) return;
      isDragging = false;
      // Add velocity inertia on release and magnetically snap to nearest integer index (infinite)
      const inertiaShift = -dragVelocity * 0.08;
      targetProgress = Math.round(targetProgress + inertiaShift);
    }

    // Dial Drag Listener
    if (dial) {
      dial.addEventListener('mousedown', (e) => {
        e.preventDefault();
        onPointerDown(e.clientX);
      });
      dial.addEventListener('touchstart', (e) => {
        if (e.touches.length > 0) onPointerDown(e.touches[0].clientX);
      }, { passive: true });
    }

    // Stage Drag Listener
    stage.addEventListener('mousedown', (e) => {
      // Don't drag if clicking buttons
      if (e.target.closest('button') || e.target.closest('a')) return;
      e.preventDefault();
      onPointerDown(e.clientX);
    });
    stage.addEventListener('touchstart', (e) => {
      if (e.target.closest('button') || e.target.closest('a')) return;
      if (e.touches.length > 0) onPointerDown(e.touches[0].clientX);
    }, { passive: true });

    window.addEventListener('mousemove', (e) => {
      if (isDragging) onPointerMove(e.clientX, 280);
    });
    window.addEventListener('touchmove', (e) => {
      if (isDragging && e.touches.length > 0) onPointerMove(e.touches[0].clientX, 280);
    }, { passive: true });

    window.addEventListener('mouseup', onPointerUp);
    window.addEventListener('touchend', onPointerUp);
    window.addEventListener('touchcancel', onPointerUp);

    // Mouse Wheel / Trackpad Scrubbing inside Orbit Section (Infinite loop)
    stage.addEventListener('wheel', (e) => {
      const delta = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
      if (Math.abs(delta) > 10) {
        e.preventDefault();
        targetProgress += (delta > 0 ? 0.35 : -0.35);

        clearTimeout(wheelSnapTimer);
        wheelSnapTimer = setTimeout(() => {
          targetProgress = Math.round(targetProgress);
        }, 120);
      }
    }, { passive: false });

    // Keyboard Arrow Navigation (Infinite loop)
    window.addEventListener('keydown', (e) => {
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        targetProgress = Math.round(targetProgress) + 1;
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        targetProgress = Math.round(targetProgress) - 1;
      }
    });

    // Initial setup
    updateProductMeta(0);

    // 60FPS Physics Engine Loop
    const SPRING_STIFFNESS = 0.14;
    const SPRING_DAMPING = 0.76;

    function physicsLoop() {
      const stageRect = stage.getBoundingClientRect();
      const stageW = stageRect.width || 1200;
      const stageH = stageRect.height || 540;

      if (!isDragging) {
        const delta = targetProgress - currentProgress;
        velocity += delta * SPRING_STIFFNESS;
        velocity *= SPRING_DAMPING;
        currentProgress += velocity;

        if (Math.abs(delta) < 0.0005 && Math.abs(velocity) < 0.0005) {
          currentProgress = targetProgress;
          velocity = 0;
        }
      } else {
        velocity *= 0.65;
        currentProgress += (targetProgress - currentProgress) * 0.45;
      }

      // Sync active item meta on integer threshold with infinite modular mapping
      const normalizedIndex = ((Math.round(currentProgress) % N) + N) % N;
      updateProductMeta(normalizedIndex);

      // Render 7 Sneakers along 3D Perspective Arc with Shortest-Arc Wrapping
      const itemW = 480;
      const itemH = 300;

      shoeItems.forEach((item) => {
        // Shortest-arc offset calculation (cyclic modular wrapping)
        const rawOffset = ((item.index - currentProgress) % N + N) % N;
        const u = rawOffset > N / 2 ? rawOffset - N : rawOffset;

        const state = evaluateSpline(u, stageW, stageH);

        const tx = state.x - itemW / 2;
        const ty = state.y - itemH / 2;

        item.el.style.transform = `translate3d(${tx.toFixed(1)}px, ${ty.toFixed(1)}px, 0) scale(${state.scale.toFixed(3)}) rotate(${state.rot.toFixed(1)}deg)`;
        item.el.style.opacity = state.opacity.toFixed(3);
        item.el.style.zIndex = state.z;

        if (item.shadow) {
          item.shadow.style.opacity = (state.opacity * 0.95).toFixed(3);
          item.shadow.style.transform = `scale(${state.scale.toFixed(3)})`;
        }

        if (Math.abs(u) < 0.4) {
          item.el.classList.add('is-hero');
        } else {
          item.el.classList.remove('is-hero');
        }
      });

      // Update Scrubber Track Thumb Indicator & Mini Preview Thumbnail
      if (indicatorTrack && indicator) {
        const trackW = indicatorTrack.clientWidth || 340;
        const cycleProgress = ((currentProgress % N) + N) % N;
        const frac = cycleProgress / (N - 1);
        const clampedFrac = Math.max(0, Math.min(1, frac));
        const thumbX = 14 + clampedFrac * (trackW - 28);

        indicator.style.left = `${thumbX.toFixed(1)}px`;

        if (thumbImg) {
          thumbImg.style.left = `${thumbX.toFixed(1)}px`;
        }
      }

      // Shift Dial Ribs with Continuous Motion (Infinite)
      if (ribs) {
        const ribShift = (-currentProgress * 55) % 36;
        ribs.style.transform = `translateX(${ribShift.toFixed(1)}px)`;
      }

      requestAnimationFrame(physicsLoop);
    }

    requestAnimationFrame(physicsLoop);
  }

  // --------------------------------------------------------------------------
  // 2. INTERACTIVE HORIZONTAL CLOTHING RACK SHOWCASE (PHYSICS & 3D ROTATION)
  // --------------------------------------------------------------------------
  const RACK_PRODUCTS = [
    {
      id: 'rack-blazer-navy-1',
      title: 'Tailored Navy Wool Blazer',
      subtitle: 'Midnight Navy',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/jacket-navy.png',
      sideImage: '/assets/hoodies/jacket-navy-side.png',
      desc: 'Structured wool blend tailored blazer featuring padded shoulders, notch lapel profile, kissing button cuffs, and a vented back. Sartorial precision for casual or formal layering.'
    },
    {
      id: 'rack-hoodie-grey-1',
      title: 'Heather Gray Heavy Hoodie',
      subtitle: 'Heather Grey',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/hoodie-grey.png',
      sideImage: '/assets/hoodies/hoodie-grey-side.png',
      desc: 'Ultra-dense brushed French terry with double-layered hood, angled sleeve drape, bent elbow contour, and kangaroo pocket edge. Vintage stone washed for a lived-in texture.'
    },
    {
      id: 'rack-hoodie-black-1',
      title: 'Charcoal Oversized Hoodie',
      subtitle: 'Washed Charcoal',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/hoodie-black.png',
      sideImage: '/assets/hoodies/hoodie-black-side.png',
      desc: 'Crafted from custom-milled 480 GSM organic cotton fleece with deep dropped shoulders, generous hood volume, and ribbed waistband drape.'
    },
    {
      id: 'rack-hoodie-cream-1',
      title: 'Vintage Oatmeal Fleece Hoodie',
      subtitle: 'Natural Ecru',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/hoodie-cream.png',
      sideImage: '/assets/hoodies/hoodie-cream-side.png',
      desc: 'Heavy-gauge organic fleece in natural unbleached ecru. Minimalist tonal embroidery on chest with natural sleeve bend and kangaroo pouch contour.'
    },
    {
      id: 'rack-hoodie-green-1',
      title: 'Pine Green Heavy Hoodie',
      subtitle: 'Forest Pine',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/hoodie-green.png',
      sideImage: '/assets/hoodies/hoodie-green-side.png',
      desc: 'Deep forest green 500 GSM loopback cotton. Bulky hood volume behind collar, pre-shrunk with garment dye treatment for rich hue depth.'
    },
    {
      id: 'rack-crew-black-1',
      title: 'Heavyweight Black Crewneck',
      subtitle: 'Pitch Black',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/hoodie-black.png',
      sideImage: '/assets/hoodies/crewneck-black-side.png',
      desc: 'Minimalist heavyweight cotton crewneck with structured short/mid sleeve profile, clean collar contour, and tubular hem drape.'
    },
    {
      id: 'rack-blazer-navy-2',
      title: 'Technical Wool Outerwear',
      subtitle: 'Deep Indigo',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/jacket-navy.png',
      sideImage: '/assets/hoodies/jacket-navy-side.png',
      desc: 'Hybrid tailored jacket with architectural cut, internal chest storm pocket, and ergonomic articulated sleeve tailoring.'
    },
    {
      id: 'rack-hoodie-grey-2',
      title: 'Ash Melange Classic Hoodie',
      subtitle: 'Ash Melange',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/hoodie-grey.png',
      sideImage: '/assets/hoodies/hoodie-grey-side.png',
      desc: 'Timeless athletic fleece with reinforced double-stitched hood, relaxed sleeve fold, and ribbed side panels for flexibility.'
    },
    {
      id: 'rack-hoodie-black-2',
      title: 'Core Stealth Pullover',
      subtitle: 'Stealth Black',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/hoodie-black.png',
      sideImage: '/assets/hoodies/hoodie-black-side.png',
      desc: 'Minimalist stealth hoodie with concealed side pockets and ribbed storm cuffs. Designed for layered technical styling.'
    },
    {
      id: 'rack-hoodie-cream-2',
      title: 'Sand Heavy Fleece Pullover',
      subtitle: 'Sand Ecru',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/hoodie-cream.png',
      sideImage: '/assets/hoodies/hoodie-cream-side.png',
      desc: 'Heavyweight organic cotton fleece with smooth face and plush interior. Cut with natural fabric volume and relaxed side drape.'
    },
    {
      id: 'rack-hoodie-green-2',
      title: 'Evergreen Heritage Hoodie',
      subtitle: 'Dark Cypress',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/hoodie-green.png',
      sideImage: '/assets/hoodies/hoodie-green-side.png',
      desc: 'Heavyweight heritage fleece inspired by archival streetwear. High density ribbed waistband and structured hood profile.'
    },
    {
      id: 'rack-crew-black-2',
      title: 'Classic Heavyweight Tee',
      subtitle: 'Washed Black',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/hoodie-black.png',
      sideImage: '/assets/hoodies/crewneck-black-side.png',
      desc: '320 GSM custom combed cotton jersey with bound ribbed neckline and straight-cut drop silhouette.'
    },
    {
      id: 'rack-blazer-navy-3',
      title: 'Artisan Tailored Jacket',
      subtitle: 'Midnight Blue',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/jacket-navy.png',
      sideImage: '/assets/hoodies/jacket-navy-side.png',
      desc: 'Tailored unstructured jacket with horn buttons, dual front patch pockets, and hand-finished lapel edges.'
    },
    {
      id: 'rack-hoodie-grey-3',
      title: 'Thermal Ribbed Hoodie',
      subtitle: 'Oatmeal Grey',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/hoodie-grey.png',
      sideImage: '/assets/hoodies/hoodie-grey-side.png',
      desc: 'Waffle thermal lined hood with heavy-gauge loopback body. Natural elbow bend and flared hem drape.'
    },
    {
      id: 'rack-hoodie-cream-3',
      title: 'Raw Edge Sand Pullover',
      subtitle: 'Desert Clay',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/hoodie-cream.png',
      sideImage: '/assets/hoodies/hoodie-cream-side.png',
      desc: 'Natural pigment dyed fleece with hand-finished raw hems, tonal drawcords, and authentic side volume.'
    },
    {
      id: 'rack-hoodie-black-3',
      title: 'Double-Layer Storm Hoodie',
      subtitle: 'Eclipse Black',
      price: '$199.00',
      numericPrice: 199,
      tag: '$199',
      frontImage: '/assets/hoodies/hoodie-black.png',
      sideImage: '/assets/hoodies/hoodie-black-side.png',
      desc: 'Fully lined with heavyweight thermal jersey. Designed for extreme durability, hood volume, and daily wear.'
    }
  ];

  function initRail() {
    const stage = document.getElementById('rack-stage');
    const hangersLayer = document.getElementById('rack-hangers-layer');
    const wirePath = document.getElementById('rack-wire-path');
    const wireSvg = document.getElementById('rack-wire-svg');
    const infoIdle = document.getElementById('rack-info-idle');
    const infoActive = document.getElementById('rack-info-active');
    const activeTitle = document.getElementById('rack-active-title');
    const activePrice = document.getElementById('rack-active-price');

    // Quick look modal elements
    const rackModal = document.getElementById('rack-modal');
    const modalClose = document.getElementById('rack-modal-close');
    const modalImg = document.getElementById('rack-modal-img');
    const modalTitle = document.getElementById('rack-modal-title');
    const modalPrice = document.getElementById('rack-modal-price');
    const modalDesc = document.getElementById('rack-modal-desc');
    const modalAddBtn = document.getElementById('rack-modal-add-btn');

    if (!stage || !hangersLayer) return;

    let activeModalProduct = null;

    if (modalClose && rackModal) {
      modalClose.addEventListener('click', () => {
        rackModal.close();
      });
      rackModal.addEventListener('click', (e) => {
        const rect = rackModal.getBoundingClientRect();
        const isInDialog = (
          rect.top <= e.clientY &&
          e.clientY <= rect.top + rect.height &&
          rect.left <= e.clientX &&
          e.clientX <= rect.left + rect.width
        );
        if (!isInDialog) {
          rackModal.close();
        }
      });
    }

    if (modalAddBtn && rackModal) {
      modalAddBtn.addEventListener('click', () => {
        if (activeModalProduct) {
          const activePill = document.querySelector('.rack-size-pill.is-active');
          const chosenSize = activePill ? activePill.textContent.trim() : 'M';
          if (window.AtelierCart) {
            window.AtelierCart.add({
              id: `rack-${activeModalProduct.id}-${chosenSize}`,
              productId: activeModalProduct.id,
              name: activeModalProduct.title,
              price: activeModalProduct.numericPrice || 199,
              size: chosenSize,
              image: activeModalProduct.frontImage || activeModalProduct.sideImage,
              quantity: 1
            });
          } else {
            triggerBagToast(`${activeModalProduct.title} (Size ${chosenSize}) added to bag`);
            incrementCartCount();
          }
          rackModal.close();
        }
      });
    }

    // Modal size pill toggle
    document.querySelectorAll('.rack-size-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        document.querySelectorAll('.rack-size-pill').forEach(p => p.classList.remove('is-active'));
        pill.classList.add('is-active');
      });
    });

    const N = RACK_PRODUCTS.length;
    let hoveredIndex = -1;
    let isDragging = false;
    let dragStartX = 0;

    // Render Hanger Items into DOM
    hangersLayer.innerHTML = '';
    const itemNodes = [];

    RACK_PRODUCTS.forEach((prod, i) => {
      const itemEl = document.createElement('div');
      itemEl.className = 'rack-hanger-item';
      itemEl.dataset.index = i;
      itemEl.setAttribute('role', 'button');
      itemEl.setAttribute('tabindex', '0');
      itemEl.setAttribute('aria-label', `${prod.title} - ${prod.price}`);

      // Price tag hangs below rail (top: 10px) with string loop and eyelet
      // Garment hook apex sits directly on the rail wire
      itemEl.innerHTML = `
        <div class="rack-price-tag" aria-hidden="true">
          <span class="rack-tag-string"></span>
          <span class="rack-tag-eyelet"></span>
          <span class="rack-tag-text">${prod.tag}</span>
        </div>
        <div class="rack-garment-wrapper">
          <div class="rack-garment-rotator">
            <img class="rack-garment-img rack-garment-side" src="${prod.sideImage}" alt="${prod.title} - Side View" loading="lazy" draggable="false" />
            <img class="rack-garment-img rack-garment-front" src="${prod.frontImage}" alt="${prod.title} - Front View" loading="lazy" draggable="false" style="opacity: 0; transform: rotateY(90deg);" />
          </div>
        </div>
      `;

      hangersLayer.appendChild(itemEl);

      itemNodes.push({
        el: itemEl,
        tagEl: itemEl.querySelector('.rack-price-tag'),
        rotatorEl: itemEl.querySelector('.rack-garment-rotator'),
        sideImgEl: itemEl.querySelector('.rack-garment-side'),
        frontImgEl: itemEl.querySelector('.rack-garment-front'),
        product: prod,
        x: 0,
        targetX: 0,
        vx: 0,
        sway: 0,
        progress: 0,
        targetProgress: 0,
        width: 58,
        targetWidth: 58
      });

      // Mouse hover events
      itemEl.addEventListener('mouseenter', () => {
        hoveredIndex = i;
        updateFooterInfo(prod);
      });

      // Click to open quick look modal
      itemEl.addEventListener('click', () => {
        openQuickLook(prod);
      });

      itemEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openQuickLook(prod);
        }
      });
    });

    stage.addEventListener('mouseleave', () => {
      hoveredIndex = -1;
      resetFooterInfo();
    });

    // Touch and drag scrubbing for mobile & desktop
    function handlePointerMove(clientX) {
      const rect = stage.getBoundingClientRect();
      const relX = clientX - rect.left;
      let closestIdx = -1;
      let minDist = Infinity;
      itemNodes.forEach((item, idx) => {
        const d = Math.abs(item.x - relX);
        if (d < minDist) {
          minDist = d;
          closestIdx = idx;
        }
      });
      if (closestIdx !== -1 && closestIdx !== hoveredIndex) {
        hoveredIndex = closestIdx;
        updateFooterInfo(RACK_PRODUCTS[closestIdx]);
      }
    }

    stage.addEventListener('touchstart', (e) => {
      isDragging = true;
      if (e.touches.length > 0) {
        dragStartX = e.touches[0].clientX;
        handlePointerMove(dragStartX);
      }
    }, { passive: true });

    stage.addEventListener('touchmove', (e) => {
      if (isDragging && e.touches.length > 0) {
        handlePointerMove(e.touches[0].clientX);
      }
    }, { passive: true });

    stage.addEventListener('touchend', () => {
      isDragging = false;
    });

    function openQuickLook(prod) {
      activeModalProduct = prod;
      if (modalImg) modalImg.src = prod.frontImage;
      if (modalTitle) modalTitle.textContent = prod.title;
      if (modalPrice) modalPrice.textContent = prod.price;
      if (modalDesc) modalDesc.textContent = prod.desc;
      if (rackModal && typeof rackModal.showModal === 'function') {
        rackModal.showModal();
      }
    }

    function updateFooterInfo(prod) {
      if (infoIdle && infoActive && activeTitle && activePrice) {
        infoIdle.classList.add('is-hidden');
        infoActive.classList.remove('is-hidden');
        activeTitle.textContent = prod.title;
        activePrice.textContent = prod.price;
      }
    }

    function resetFooterInfo() {
      if (infoIdle && infoActive) {
        infoActive.classList.add('is-hidden');
        infoIdle.classList.remove('is-hidden');
      }
    }

    // Geometry & Wire Parabola
    let stageWidth = stage.clientWidth || 1400;
    const y0 = 24;      // Elevation at left/right edges
    const droop = 28;   // Downward sag in middle

    function updateWireSVG() {
      stageWidth = stage.clientWidth || 1400;
      if (wirePath && wireSvg) {
        wireSvg.setAttribute('viewBox', `0 0 ${stageWidth} 80`);
        const midY = y0 + 2 * droop;
        wirePath.setAttribute('d', `M 0 ${y0} Q ${stageWidth / 2} ${midY} ${stageWidth} ${y0}`);
      }
    }

    function getRailY(x) {
      const halfW = stageWidth / 2;
      const norm = (x - halfW) / halfW;
      return y0 + droop * (1.0 - norm * norm);
    }

    function getRailAngle(x) {
      const halfW = stageWidth / 2;
      const slope = -2.0 * droop * (x - halfW) / (halfW * halfW);
      return Math.atan(slope) * (180 / Math.PI);
    }

    // Compute resting (72px spacing) and accordion target positions
    function computeTargets() {
      stageWidth = stage.clientWidth || 1400;

      // Pack garments closely at ~72px center-to-center spacing (14px whitespace between 58px wide items)
      const targetSpacing = Math.min(72, (stageWidth - 140) / (N - 1));
      const totalSpan = (N - 1) * targetSpacing;
      const startX = (stageWidth - totalSpan) / 2;

      if (hoveredIndex === -1) {
        // Resting state: 58px natural width, rotateY(0deg), NO squishing!
        for (let i = 0; i < N; i++) {
          itemNodes[i].targetX = startX + i * targetSpacing;
          itemNodes[i].targetWidth = 58;
          itemNodes[i].targetProgress = 0.0;
          itemNodes[i].el.classList.remove('is-hovered');
        }
        return;
      }

      // Accordion Push Effect: active garment expands from 58px to 220px
      const hIdx = hoveredIndex;
      const restingW = 58;
      const expandedW = 220; // 210px–230px range
      const extraSpaceNeeded = expandedW - restingW; // ~162px

      const minX = 40;
      const maxX = stageWidth - 40;

      const baseCenter = startX + hIdx * targetSpacing;
      const leftCount = hIdx;
      const rightCount = (N - 1) - hIdx;

      // Proportional push offsets
      const availLeft = Math.max(10, baseCenter - minX - leftCount * 36);
      const availRight = Math.max(10, maxX - baseCenter - rightCount * 36);
      const totalAvail = availLeft + availRight;

      const shiftLeft = extraSpaceNeeded * (availLeft / totalAvail);
      const shiftRight = extraSpaceNeeded * (availRight / totalAvail);

      for (let i = 0; i < N; i++) {
        const item = itemNodes[i];
        const baseX = startX + i * targetSpacing;

        if (i < hIdx) {
          const factor = (i + 1) / (leftCount + 1);
          item.targetX = baseX - shiftLeft * factor;
          item.targetWidth = 58;
          item.targetProgress = 0.0;
          item.el.classList.remove('is-hovered');
        } else if (i > hIdx) {
          const factor = (N - i) / (rightCount + 1);
          item.targetX = baseX + shiftRight * factor;
          item.targetWidth = 58;
          item.targetProgress = 0.0;
          item.el.classList.remove('is-hovered');
        } else {
          item.targetX = baseX;
          item.targetWidth = expandedW;
          item.targetProgress = 1.0;
          item.el.classList.add('is-hovered');
        }
      }
    }

    // Initialize initial positions
    updateWireSVG();
    computeTargets();
    itemNodes.forEach(item => {
      item.x = item.targetX;
      item.width = item.targetWidth;
      item.progress = item.targetProgress;
      item.el.style.width = `${item.width}px`;
      item.el.style.marginLeft = `${-item.width / 2}px`;
    });

    window.addEventListener('resize', () => {
      updateWireSVG();
      computeTargets();
    });

    // 60FPS Spring-Based Physics Loop
    const SPRING_K = 0.14;
    const DAMPING = 0.78;

    let isRunning = true;

    function physicsLoop() {
      if (!isRunning) return;

      computeTargets();

      for (let i = 0; i < N; i++) {
        const item = itemNodes[i];

        // Spring position displacement
        const ax = (item.targetX - item.x) * SPRING_K;
        item.vx = (item.vx + ax) * DAMPING;
        item.x += item.vx;

        // Smooth container width expansion (58px -> 220px)
        item.width += (item.targetWidth - item.width) * 0.18;
        item.el.style.width = `${item.width.toFixed(1)}px`;
        item.el.style.marginLeft = `${(-item.width / 2).toFixed(1)}px`;

        // Velocity-driven pendulum sway
        const targetSway = Math.max(-10, Math.min(10, item.vx * -1.5));
        item.sway += (targetSway - item.sway) * 0.16;

        // Smooth 3D rotational transition progress (0.0 at rest, 1.0 when hovered)
        item.progress += (item.targetProgress - item.progress) * 0.18;
        const P = item.progress;

        // True 3D Turn:
        // Side profile starts at 0deg at rest (FULL natural width, NO squishing!)
        // Turns out: 0deg -> 90deg, opacity: 1 -> 0
        // Front profile turns in: 90deg -> 0deg, opacity: 0 -> 1
        // Midpoint swap at P = 0.5 (45deg)
        const rotSide = P * 90;
        const rotFront = (1 - P) * 90;

        const opSide = Math.max(0, Math.min(1, 1 - P * 2.2));
        const opFront = Math.max(0, Math.min(1, (P - 0.45) * 2.2));

        item.sideImgEl.style.transform = `rotateY(${rotSide.toFixed(2)}deg)`;
        item.sideImgEl.style.opacity = opSide.toFixed(3);

        item.frontImgEl.style.transform = `rotateY(${-rotFront.toFixed(2)}deg)`;
        item.frontImgEl.style.opacity = opFront.toFixed(3);

        // Parabolic geometry coordinates
        const curY = getRailY(item.x);
        const tangentAngle = getRailAngle(item.x);

        // Hardware-accelerated GPU transforms:
        // Hook wraps directly over wire rail with zero gap
        item.el.style.transform = `translate3d(${item.x.toFixed(2)}px, ${curY.toFixed(2)}px, 0)`;
        // Tag tilts below rail along the wire's tangent angle
        item.tagEl.style.transform = `translateX(-50%) rotate(${(tangentAngle + item.sway * 1.1).toFixed(2)}deg)`;
      }

      requestAnimationFrame(physicsLoop);
    }

    requestAnimationFrame(physicsLoop);
  }

  // --------------------------------------------------------------------------
  // 3. GLOBAL CART HELPER
  // --------------------------------------------------------------------------
  function incrementCartCount() {
    if (window.AtelierCart) {
      const count = window.AtelierCart.getCount();
      document.querySelectorAll('[data-cart-count]').forEach((b) => {
        b.textContent = String(count);
      });
      return;
    }
    const badges = document.querySelectorAll('[data-cart-count]');
    badges.forEach((b) => {
      const current = Number(b.textContent.trim()) || 0;
      b.textContent = String(current + 1);
    });
  }

  function triggerBagToast(msg) {
    let status = document.getElementById('bag-status');
    if (!status) {
      status = document.createElement('div');
      status.id = 'bag-status';
      document.body.appendChild(status);
    }
    status.textContent = msg;
    status.classList.add('is-on');
    setTimeout(() => {
      status.classList.remove('is-on');
    }, 2800);
  }

  // --------------------------------------------------------------------------
  // 4. SMOOTH NAV LINK JUMPING
  // --------------------------------------------------------------------------
  function initNav() {
    document.querySelectorAll('.main-nav a').forEach((link) => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        if (href && href.startsWith('#')) {
          e.preventDefault();
          const target = document.querySelector(href);
          if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
            document.querySelectorAll('.main-nav a').forEach((a) => a.classList.remove('is-active'));
            link.classList.add('is-active');
          }
        }
      });
    });
  }

  // Run on DOM load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initOrbit();
      initRail();
      initNav();
    });
  } else {
    initOrbit();
    initRail();
    initNav();
  }
})();
