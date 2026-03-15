
    // ── Utilidad: leer la cookie CSRF que Django inyecta en el navegador ──
    // Django requiere este token en TODOS los POST para evitar ataques CSRF.
    function getCsrfToken() {
        const name = 'csrftoken';
        const cookie = document.cookie.split(';').find(c => c.trim().startsWith(name + '='));
        return cookie ? decodeURIComponent(cookie.trim().split('=')[1]) : '';
    }

    // ── Utilidad: mostrar un toast de notificación ──────────────────────
    function showToast(msg, isError = false) {
        const toast = document.getElementById('toast');
        const toastMsg = document.getElementById('toast-msg');
        const toastIcon = document.getElementById('toast-icon');

        toastMsg.textContent = msg;
        toastIcon.textContent = isError ? '✕' : '✓';
        toast.classList.toggle('bg-red-600', isError);
        toast.classList.toggle('bg-carbon', !isError);

        // Animar entrada
        toast.style.transform = 'translateX(0)';
        // Animar salida después de 2.5s
        setTimeout(() => { toast.style.transform = 'translateX(120%)'; }, 2500);
    }

    // ── Función POST genérica con fetch ─────────────────────────────────
    // Centraliza la lógica de llamadas AJAX para no repetirla en cada acción.
    async function postToCart(url, body = {}) {
        const res = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),   // Header requerido por Django
            },
            body: JSON.stringify(body),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
    }

    // ── Actualiza el badge de items en el navbar (si existe) ────────────
    function updateNavBadge(count) {
        const badge = document.getElementById('nav-cart-badge');
        if (badge) badge.textContent = count;
    }

    // ── Eliminar un ítem del carrito ─────────────────────────────────────
    // Enviamos POST a /carrito/eliminar/<id>/
    // Si la respuesta es exitosa, removemos la tarjeta del DOM con animación.
    async function removeItem(itemId) {
        try {
            const data = await postToCart(`/carrito/eliminar/${itemId}/`);
            if (data.success) {
                const el = document.getElementById(`item-${itemId}`);
                // Animación de salida antes de remover del DOM
                el.style.transition = 'opacity 0.25s, transform 0.25s';
                el.style.opacity = '0';
                el.style.transform = 'translateX(20px)';
                setTimeout(() => {
                    el.remove();
                    checkEmptyCart();
                }, 250);
                // Actualizar total en el resumen lateral
                document.getElementById('summary-subtotal').textContent = `$${data.cart_total}`;
                document.getElementById('summary-total').textContent = `$${data.cart_total}`;
                showToast('Producto eliminado');
            }
        } catch (e) {
            showToast('Error al eliminar', true);
        }
    }

    // ── Vaciar todo el carrito ───────────────────────────────────────────
    async function clearCart() {
        if (!confirm('¿Vaciar todo el carrito?')) return;
        try {
            const data = await postToCart('/carrito/vaciar/');
            if (data.success) {
                // Remover todos los ítems del DOM
                document.querySelectorAll('.cart-item').forEach(el => el.remove());
                checkEmptyCart();
                showToast('Carrito vaciado');
            }
        } catch (e) {
            showToast('Error al vaciar', true);
        }
    }

    // ── Verificar si el carrito quedó vacío tras una acción ─────────────
    // Si no quedan ítems, mostramos el estado vacío dinámicamente.
    function checkEmptyCart() {
        const container = document.getElementById('cart-items-container');
        const items = container.querySelectorAll('.cart-item');
        if (items.length === 0) {
            container.innerHTML = `
                <div class="bg-white rounded-3xl p-12 text-center border border-gray-100 shadow-sm">
                    <div class="text-7xl mb-4">🛒</div>
                    <h2 class="text-xl font-extrabold text-carbon mb-2">Tu carrito está vacío</h2>
                    <p class="text-ceniza text-sm mb-6">¡Agrega algo delicioso!</p>
                    <a href="/tienda/" class="inline-block bg-rappi text-white font-bold
                       px-8 py-3 rounded-xl hover:bg-rappiSoft transition">Ver el menú</a>
                </div>`;
            // Resetear el panel de resumen
            document.getElementById('summary-subtotal').textContent = '$0';
            document.getElementById('summary-total').textContent = '$0';
        }
    }

    // ── Registrar todos los event listeners al cargar el DOM ────────────
    document.addEventListener('DOMContentLoaded', () => {

        // Botón "Vaciar carrito"
        const btnClear = document.getElementById('btn-clear-cart');
        if (btnClear) btnClear.addEventListener('click', clearCart);

        // Botones "Eliminar ítem" (delegación de eventos en el contenedor)
        // Usamos delegación en lugar de un listener por botón para mayor rendimiento.
        document.getElementById('cart-items-container')
            .addEventListener('click', async (e) => {

                // Detectar click en botón de eliminar
                const removeBtn = e.target.closest('.btn-remove-item');
                if (removeBtn) {
                    await removeItem(removeBtn.dataset.itemId);
                }

                // Detectar click en botón de RESTAR cantidad
                const minusBtn = e.target.closest('.btn-qty-minus');
                if (minusBtn) {
                    const itemId = minusBtn.dataset.itemId;
                    const qtyEl = minusBtn.nextElementSibling; // El span con la cantidad
                    let qty = parseInt(qtyEl.textContent);

                    if (qty <= 1) {
                        // Si llega a 0, eliminar el ítem directamente
                        await removeItem(itemId);
                    } else {
                        qty--;
                        qtyEl.textContent = qty;
                        updateSubtotal(itemId, qty);
                        // En producción: llamar al backend para persistir el cambio
                    }
                }

                // Detectar click en botón de SUMAR cantidad
                const plusBtn = e.target.closest('.btn-qty-plus');
                if (plusBtn) {
                    const itemId = plusBtn.dataset.itemId;
                    const qtyEl = plusBtn.previousElementSibling;
                    let qty = parseInt(qtyEl.textContent);
                    if (qty < 99) {
                        qty++;
                        qtyEl.textContent = qty;
                        updateSubtotal(itemId, qty);
                    }
                }
            });
    });

    // ── Recalcular subtotal del ítem y el total del resumen ─────────────
    // Se ejecuta localmente (sin llamar al backend) para dar feedback inmediato.
    // En producción, también harías un debounce + POST al backend.
    function updateSubtotal(itemId, newQty) {
        const card = document.getElementById(`item-${itemId}`);
        const unitPrice = parseFloat(card.dataset.price);
        const subtotal = (unitPrice * newQty).toLocaleString('es-CO');

        // Actualizar subtotal del ítem
        card.querySelector('.item-subtotal').textContent = `$${subtotal}`;

        // Recalcular total sumando todos los subtotales visibles
        let total = 0;
        document.querySelectorAll('.cart-item').forEach(el => {
            const price = parseFloat(el.dataset.price);
            const qty = parseInt(el.querySelector('.qty-display').textContent);
            total += price * qty;
        });

        document.getElementById('summary-subtotal').textContent =
            `$${total.toLocaleString('es-CO')}`;
        document.getElementById('summary-total').textContent =
            `$${total.toLocaleString('es-CO')}`;
    }
