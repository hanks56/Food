/**
 * main.js - Lógica global (landing, navbar, etc.)
 */

document.addEventListener('DOMContentLoaded', function () {
    const orderBtn = document.getElementById('btn-order');

    if (orderBtn) {
        orderBtn.addEventListener('click', function () {
            orderBtn.innerHTML = "¡Añadiendo al carrito! 🛒";
            orderBtn.classList.replace('bg-rappi', 'bg-carbon');

            setTimeout(function () {
                alert('¡Pronto recibirás tu deliciosa comida!');
                orderBtn.innerHTML = "Pedir ahora";
                orderBtn.classList.replace('bg-carbon', 'bg-rappi');
            }, 1000);
        });
    }

    window.addEventListener('scroll', function () {
        const nav = document.querySelector('nav');
        if (!nav) return;
        if (window.scrollY > 50) {
            nav.classList.add('shadow-md', 'py-2');
            nav.classList.remove('py-4');
        } else {
            nav.classList.remove('shadow-md', 'py-2');
            nav.classList.add('py-4');
        }
    });
});
