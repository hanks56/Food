/**
 * catalog.js
 * Lógica del catálogo: menú hamburguesa, modal de producto, carrito AJAX.
 *
 * FIX PRINCIPAL:
 *   1. window.IS_AUTHENTICATED lo inyecta el template Django.
 *   2. Al pulsar "Agregar al carrito", lo PRIMERO es leer esa variable.
 *   3. Si es false → abre modal de login, NUNCA hace fetch.
 *   4. Si es true  → fetch normal. Django devuelve JSON, no HTML.
 *   Esto evita el SyntaxError: Unexpected token '<' al parsear HTML como JSON.
 */
(function () {
    'use strict';

    function formatPrice(n) {
        return new Intl.NumberFormat('es-CO').format(n);
    }

    function getCsrfToken() {
        const cookie = document.cookie
            .split(';')
            .find(c => c.trim().startsWith('csrftoken='));
        return cookie ? decodeURIComponent(cookie.trim().split('=')[1]) : '';
    }

    function showToast(msg, isError = false) {
        let toast = document.getElementById('cart-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'cart-toast';
            toast.style.cssText = 'position:fixed;top:24px;right:24px;z-index:9999;display:flex;align-items:center;gap:10px;padding:14px 20px;border-radius:16px;font-size:14px;font-weight:600;color:#fff;box-shadow:0 8px 32px rgba(0,0,0,0.18);transition:transform 0.35s cubic-bezier(.34,1.56,.64,1),opacity 0.3s;transform:translateX(120%);opacity:0;';
            document.body.appendChild(toast);
        }
        toast.style.background = isError ? '#ef4444' : '#1A1A1B';
        toast.innerHTML = `<span>${isError ? '✕' : '✓'}</span><span>${msg}</span>`;
        requestAnimationFrame(() => {
            toast.style.transform = 'translateX(0)';
            toast.style.opacity   = '1';
        });
        clearTimeout(toast._t);
        toast._t = setTimeout(() => {
            toast.style.transform = 'translateX(120%)';
            toast.style.opacity   = '0';
        }, 2500);
    }

    function updateCartBadge(count) {
        const badge = document.getElementById('nav-cart-badge');
        if (!badge) return;
        badge.textContent   = count;
        badge.style.display = count > 0 ? 'flex' : 'none';
    }

    // ── Modal de login requerido ──────────────────────────────────────────
    function initLoginModal() {
        const modal    = document.getElementById('login-required-modal');
        const backdrop = document.getElementById('login-modal-backdrop');
        const closeBtn = document.getElementById('login-modal-close');
        if (!modal) return;

        function openLoginModal() {
            modal.classList.remove('opacity-0', 'pointer-events-none');
            modal.classList.add('pointer-events-auto');
            document.body.style.overflow = 'hidden';
        }
        function closeLoginModal() {
            modal.classList.add('opacity-0', 'pointer-events-none');
            modal.classList.remove('pointer-events-auto');
            document.body.style.overflow = '';
        }

        if (closeBtn)  closeBtn.addEventListener('click', closeLoginModal);
        if (backdrop)  backdrop.addEventListener('click', closeLoginModal);
        document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLoginModal(); });

        window._openLoginModal = openLoginModal;
    }

    // ── Menú hamburguesa ─────────────────────────────────────────────────
    function initHamburgerMenu() {
        const btnMenu       = document.getElementById('btn-menu-hamburger');
        const sidebar       = document.getElementById('sidebar');
        const overlay       = document.getElementById('sidebar-overlay');
        const iconHamburger = document.getElementById('icon-hamburger');
        const iconClose     = document.getElementById('icon-close');
        if (!btnMenu || !sidebar) return;

        function openSidebar() {
            sidebar.classList.remove('-translate-x-full');
            overlay.classList.remove('opacity-0', 'pointer-events-none');
            if (iconHamburger) iconHamburger.classList.add('hidden');
            if (iconClose)     iconClose.classList.remove('hidden');
        }
        function closeSidebar() {
            sidebar.classList.add('-translate-x-full');
            overlay.classList.add('opacity-0', 'pointer-events-none');
            if (iconHamburger) iconHamburger.classList.remove('hidden');
            if (iconClose)     iconClose.classList.add('hidden');
        }

        btnMenu.addEventListener('click', () =>
            sidebar.classList.contains('-translate-x-full') ? openSidebar() : closeSidebar()
        );
        overlay.addEventListener('click', closeSidebar);
        document.querySelectorAll('.category-link').forEach(link =>
            link.addEventListener('click', closeSidebar)
        );
    }

    // ── Modal de producto + carrito ───────────────────────────────────────
    function initProductModal() {
        const productModal     = document.getElementById('product-modal');
        const modalBackdrop    = document.getElementById('product-modal-backdrop');
        const modalClose       = document.getElementById('product-modal-close');
        const modalImage       = document.getElementById('modal-product-image');
        const modalName        = document.getElementById('modal-product-name');
        const modalDescription = document.getElementById('modal-product-description');
        const modalPrice       = document.getElementById('modal-product-price');
        const productQty       = document.getElementById('product-qty');
        const qtyMinus         = document.getElementById('qty-minus');
        const qtyPlus          = document.getElementById('qty-plus');
        const btnAddToCart     = document.getElementById('btn-add-to-cart');
        if (!productModal) return;

        let currentProductId = null;

        function openProductModal(card) {
            currentProductId = card.dataset.id;
            if (modalImage) { modalImage.src = card.dataset.image || ''; modalImage.alt = card.dataset.name || ''; }
            if (modalName)          modalName.textContent        = card.dataset.name        || '';
            if (modalDescription)   modalDescription.textContent = card.dataset.description || '';
            if (modalPrice)         modalPrice.textContent       = '$' + formatPrice(parseInt(card.dataset.price, 10) || 0);
            if (productQty)         productQty.value             = 1;
            const cb = document.getElementById('product-cubiertos');
            if (cb) cb.checked = false;
            productModal.classList.remove('opacity-0', 'pointer-events-none');
            productModal.classList.add('pointer-events-auto');
            document.body.style.overflow = 'hidden';
        }

        function closeProductModal() {
            productModal.classList.add('opacity-0', 'pointer-events-none');
            productModal.classList.remove('pointer-events-auto');
            document.body.style.overflow = '';
            currentProductId = null;
        }

        document.querySelectorAll('.product-card').forEach(card =>
            card.addEventListener('click', () => openProductModal(card))
        );
        if (modalClose)    modalClose.addEventListener('click', closeProductModal);
        if (modalBackdrop) modalBackdrop.addEventListener('click', closeProductModal);
        document.addEventListener('keydown', e => { if (e.key === 'Escape') closeProductModal(); });

        if (qtyMinus) qtyMinus.addEventListener('click', () => { const v = parseInt(productQty.value,10); if(v>1) productQty.value=v-1; });
        if (qtyPlus)  qtyPlus.addEventListener('click',  () => { const v = parseInt(productQty.value,10); if(v<99) productQty.value=v+1; });
        if (productQty) {
            productQty.addEventListener('change', () => {
                let v = parseInt(productQty.value, 10);
                if (isNaN(v) || v < 1) v = 1;
                if (v > 99) v = 99;
                productQty.value = v;
            });
        }

        if (!btnAddToCart) return;

        btnAddToCart.addEventListener('click', async function () {

            // ═══════════════════════════════════════════════════════════
            // VERIFICACIÓN DE AUTENTICACIÓN — va PRIMERO, antes del fetch
            // Esto es lo que evita el SyntaxError del JSON.parse
            // ═══════════════════════════════════════════════════════════
            if (!window.IS_AUTHENTICATED) {
                closeProductModal();
                setTimeout(() => {
                    if (typeof window._openLoginModal === 'function') {
                        window._openLoginModal();
                    } else {
                        window.location.href = '/usuarios/login/';
                    }
                }, 180);
                return; // ← Nunca llega al fetch
            }

            if (!currentProductId) {
                showToast('No se pudo identificar el producto', true);
                return;
            }

            const qty = parseInt(productQty.value, 10);
            const cb  = document.getElementById('product-cubiertos');

            btnAddToCart.disabled    = true;
            btnAddToCart.textContent = 'Agregando...';

            try {
                const response = await fetch('/carrito/agregar/', {
                    method:  'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken':  getCsrfToken(),
                    },
                    body: JSON.stringify({
                        product_id:    currentProductId,
                        quantity:      qty,
                        needs_cutlery: cb ? cb.checked : false,
                    }),
                });

                // Segunda defensa: si Django devolvió HTML en vez de JSON
                // (ej: sesión expirada), lo detectamos por el Content-Type
                const ct = response.headers.get('content-type') || '';
                if (!ct.includes('application/json')) {
                    showToast('Tu sesión expiró. Inicia sesión de nuevo.', true);
                    setTimeout(() => { window.location.href = '/usuarios/login/'; }, 1800);
                    return;
                }

                const data = await response.json();

                if (data.success) {
                    updateCartBadge(data.cart_total_items);
                    showToast('✓ Agregado al carrito');
                    closeProductModal();
                } else {
                    showToast(data.error || 'Error al agregar', true);
                }

            } catch (err) {
                console.error('Error al agregar al carrito:', err);
                showToast('Error de conexión', true);
            } finally {
                btnAddToCart.disabled    = false;
                btnAddToCart.textContent = 'Agregar al carrito';
            }
        });
    }

    function init() {
        initLoginModal();
        initHamburgerMenu();
        initProductModal();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();