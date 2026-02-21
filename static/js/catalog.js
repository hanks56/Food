/**
 * catalog.js - Lógica del catálogo de productos
 * Menú hamburguesa, modal de producto y conexión real con el carrito (backend Django)
 */
(function () {
    'use strict';

    // ── Formatea números al estilo colombiano: 14000 → "14.000" ──────────
    function formatPrice(n) {
        return new Intl.NumberFormat('es-CO').format(n) + '';
    }

    // ── Lee la cookie csrftoken que Django inyecta en el navegador ────────
    // Sin este token, Django rechaza cualquier POST con error 403 Forbidden.
    function getCsrfToken() {
        const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
        return cookie ? decodeURIComponent(cookie.trim().split('=')[1]) : '';
    }

    // ── Toast de notificación (feedback visual de acciones del carrito) ───
    function showToast(msg, isError = false) {
        // Crear el toast si no existe en el DOM
        let toast = document.getElementById('cart-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'cart-toast';
            toast.style.cssText = `
                position:fixed; top:24px; right:24px; z-index:9999;
                display:flex; align-items:center; gap:10px;
                padding:14px 20px; border-radius:16px;
                font-size:14px; font-weight:600; color:#fff;
                box-shadow:0 8px 32px rgba(0,0,0,0.18);
                transition: transform 0.35s cubic-bezier(.34,1.56,.64,1), opacity 0.3s;
                transform: translateX(120%); opacity:0;
            `;
            document.body.appendChild(toast);
        }
        toast.style.background = isError ? '#ef4444' : '#1A1A1B';
        toast.innerHTML = `<span>${isError ? '✕' : '✓'}</span><span>${msg}</span>`;

        // Animar entrada
        requestAnimationFrame(() => {
            toast.style.transform = 'translateX(0)';
            toast.style.opacity = '1';
        });
        // Animar salida después de 2.5s
        clearTimeout(toast._hideTimer);
        toast._hideTimer = setTimeout(() => {
            toast.style.transform = 'translateX(120%)';
            toast.style.opacity = '0';
        }, 2500);
    }

    // ── Actualiza el badge del carrito en el navbar ───────────────────────
    function updateCartBadge(count) {
        const badge = document.getElementById('nav-cart-badge');
        if (!badge) return;
        badge.textContent = count;
        // Mostrar u ocultar según si hay items
        badge.style.display = count > 0 ? 'flex' : 'none';
    }

    // ── Menú hamburguesa de la barra lateral ─────────────────────────────
    function initHamburgerMenu() {
        const btnMenu      = document.getElementById('btn-menu-hamburger');
        const sidebar      = document.getElementById('sidebar');
        const overlay      = document.getElementById('sidebar-overlay');
        const iconHamburger = document.getElementById('icon-hamburger');
        const iconClose    = document.getElementById('icon-close');
        if (!btnMenu || !sidebar) return;

        function openSidebar() {
            sidebar.classList.remove('-translate-x-full');
            overlay.classList.remove('opacity-0', 'pointer-events-none');
            if (iconHamburger) iconHamburger.classList.add('hidden');
            if (iconClose) iconClose.classList.remove('hidden');
        }
        function closeSidebar() {
            sidebar.classList.add('-translate-x-full');
            overlay.classList.add('opacity-0', 'pointer-events-none');
            if (iconHamburger) iconHamburger.classList.remove('hidden');
            if (iconClose) iconClose.classList.add('hidden');
        }

        btnMenu.addEventListener('click', () => {
            sidebar.classList.contains('-translate-x-full') ? openSidebar() : closeSidebar();
        });
        overlay.addEventListener('click', closeSidebar);
        document.querySelectorAll('.category-link').forEach(link => {
            link.addEventListener('click', closeSidebar);
        });
    }

    // ── Modal de producto + lógica de carrito ─────────────────────────────
    function initProductModal() {
        const productModal    = document.getElementById('product-modal');
        const modalBackdrop   = document.getElementById('product-modal-backdrop');
        const modalClose      = document.getElementById('product-modal-close');
        const modalImage      = document.getElementById('modal-product-image');
        const modalName       = document.getElementById('modal-product-name');
        const modalDescription = document.getElementById('modal-product-description');
        const modalPrice      = document.getElementById('modal-product-price');
        const productQty      = document.getElementById('product-qty');
        const qtyMinus        = document.getElementById('qty-minus');
        const qtyPlus         = document.getElementById('qty-plus');
        const btnAddToCart    = document.getElementById('btn-add-to-cart');
        if (!productModal) return;

        // Guardamos el product_id del producto actualmente abierto en el modal.
        // Este valor viene del atributo data-id de cada tarjeta (catalog.html).
        let currentProductId = null;

        function openProductModal(card) {
            // Leer los data-* de la tarjeta del producto
            currentProductId      = card.dataset.id;          // ← ID para el backend
            const name            = card.dataset.name;
            const description     = card.dataset.description;
            const price           = parseInt(card.dataset.price, 10);
            const image           = card.dataset.image;

            if (modalImage)       { modalImage.src = image || ''; modalImage.alt = name || ''; }
            if (modalName)          modalName.textContent = name || '';
            if (modalDescription)   modalDescription.textContent = description || '';
            if (modalPrice)         modalPrice.textContent = '$' + formatPrice(price || 0);
            if (productQty)         productQty.value = 1;

            const cubiertosCheck = document.getElementById('product-cubiertos');
            if (cubiertosCheck) cubiertosCheck.checked = false;

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

        // Abrir modal al hacer click en una tarjeta de producto
        document.querySelectorAll('.product-card').forEach(card => {
            card.addEventListener('click', () => openProductModal(card));
        });

        // Cerrar modal
        if (modalClose)   modalClose.addEventListener('click', closeProductModal);
        if (modalBackdrop) modalBackdrop.addEventListener('click', closeProductModal);
        document.addEventListener('keydown', e => { if (e.key === 'Escape') closeProductModal(); });

        // Controles de cantidad dentro del modal
        if (qtyMinus) {
            qtyMinus.addEventListener('click', () => {
                const v = parseInt(productQty.value, 10);
                if (v > 1) productQty.value = v - 1;
            });
        }
        if (qtyPlus) {
            qtyPlus.addEventListener('click', () => {
                const v = parseInt(productQty.value, 10);
                if (v < 99) productQty.value = v + 1;
            });
        }
        if (productQty) {
            productQty.addEventListener('change', () => {
                let v = parseInt(productQty.value, 10);
                if (isNaN(v) || v < 1) v = 1;
                if (v > 99) v = 99;
                productQty.value = v;
            });
        }

        // ── BOTÓN "AGREGAR AL CARRITO" → llama al backend ────────────────
        if (btnAddToCart) {
            btnAddToCart.addEventListener('click', async function () {

                // Verificar que el usuario está logueado: si no hay product_id
                // o si Django redirige al login, lo manejamos aquí.
                if (!currentProductId) {
                    showToast('No se pudo identificar el producto', true);
                    return;
                }

                const qty          = parseInt(productQty.value, 10);
                const cubiertosCheck = document.getElementById('product-cubiertos');
                const cubiertos    = cubiertosCheck ? cubiertosCheck.checked : false;

                // Deshabilitar el botón mientras se procesa para evitar doble click
                btnAddToCart.disabled = true;
                btnAddToCart.textContent = 'Agregando...';

                try {
                    // POST a /carrito/agregar/ con los datos del producto
                    const response = await fetch('/carrito/agregar/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            // Header requerido por Django para validar que la
                            // petición viene del mismo sitio y no es un ataque CSRF
                            'X-CSRFToken': getCsrfToken(),
                        },
                        body: JSON.stringify({
                            product_id:    currentProductId,
                            quantity:      qty,
                            needs_cutlery: cubiertos,
                        }),
                    });

                    const data = await response.json();

                    if (data.success) {
                        // Actualizar el badge del navbar con la nueva cantidad total
                        updateCartBadge(data.cart_total_items);
                        showToast(`✓ Agregado al carrito`);
                        closeProductModal();
                    } else if (response.status === 302 || response.redirected) {
                        // Django redirigió al login → el usuario no está autenticado
                        showToast('Inicia sesión para agregar al carrito', true);
                        setTimeout(() => { window.location.href = '/usuarios/login/'; }, 1500);
                    } else {
                        showToast(data.error || 'Error al agregar', true);
                    }

                } catch (err) {
                    // Error de red o servidor caído
                    console.error('Error al agregar al carrito:', err);
                    showToast('Error de conexión', true);
                } finally {
                    // Siempre rehabilitar el botón al terminar
                    btnAddToCart.disabled = false;
                    btnAddToCart.textContent = 'Agregar al carrito';
                }
            });
        }
    }

    // ── Punto de entrada ──────────────────────────────────────────────────
    function init() {
        initHamburgerMenu();
        initProductModal();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();