/**
 * catalog.js - Lógica del catálogo de productos
 * Menú hamburguesa, modal de producto y controles de cantidad/cubiertos
 */

(function () {
    'use strict';

    function formatPrice(n) {
        return new Intl.NumberFormat('es-CO').format(n) + '';
    }

    function initHamburgerMenu() {
        const btnMenu = document.getElementById('btn-menu-hamburger');
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        const iconHamburger = document.getElementById('icon-hamburger');
        const iconClose = document.getElementById('icon-close');

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

        document.querySelectorAll('.category-link').forEach(function (link) {
            link.addEventListener('click', closeSidebar);
        });
    }

    function initProductModal() {
        const productModal = document.getElementById('product-modal');
        const modalBackdrop = document.getElementById('product-modal-backdrop');
        const modalClose = document.getElementById('product-modal-close');
        const modalImage = document.getElementById('modal-product-image');
        const modalName = document.getElementById('modal-product-name');
        const modalDescription = document.getElementById('modal-product-description');
        const modalPrice = document.getElementById('modal-product-price');
        const productQty = document.getElementById('product-qty');
        const qtyMinus = document.getElementById('qty-minus');
        const qtyPlus = document.getElementById('qty-plus');
        const btnAddToCart = document.getElementById('btn-add-to-cart');

        if (!productModal) return;

        function openProductModal(card) {
            const name = card.dataset.name;
            const description = card.dataset.description;
            const price = parseInt(card.dataset.price, 10);
            const image = card.dataset.image;

            if (modalImage) {
                modalImage.src = image || '';
                modalImage.alt = name || '';
            }
            if (modalName) modalName.textContent = name || '';
            if (modalDescription) modalDescription.textContent = description || '';
            if (modalPrice) modalPrice.textContent = '$' + formatPrice(price || 0);
            if (productQty) productQty.value = 1;

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
        }

        document.querySelectorAll('.product-card').forEach(function (card) {
            card.addEventListener('click', function () {
                openProductModal(card);
            });
        });

        if (modalClose) modalClose.addEventListener('click', closeProductModal);
        if (modalBackdrop) modalBackdrop.addEventListener('click', closeProductModal);

        productModal.addEventListener('click', function (e) {
            if (e.target === productModal) closeProductModal();
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') closeProductModal();
        });

        if (qtyMinus) {
            qtyMinus.addEventListener('click', function () {
                const v = parseInt(productQty.value, 10);
                if (v > 1) productQty.value = v - 1;
            });
        }

        if (qtyPlus) {
            qtyPlus.addEventListener('click', function () {
                const v = parseInt(productQty.value, 10);
                if (v < 99) productQty.value = v + 1;
            });
        }

        if (productQty) {
            productQty.addEventListener('change', function () {
                let v = parseInt(productQty.value, 10);
                if (isNaN(v) || v < 1) v = 1;
                if (v > 99) v = 99;
                productQty.value = v;
            });
        }

        if (btnAddToCart) {
            btnAddToCart.addEventListener('click', function () {
                const qty = parseInt(productQty.value, 10);
                const cubiertosCheck = document.getElementById('product-cubiertos');
                const cubiertos = cubiertosCheck ? cubiertosCheck.checked : false;
                // Aquí irá la lógica del carrito más adelante
                console.log('Agregar al carrito:', {
                    nombre: modalName ? modalName.textContent : '',
                    cantidad: qty,
                    cubiertos: cubiertos
                });
                closeProductModal();
            });
        }
    }

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
