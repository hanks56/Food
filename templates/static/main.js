// static/js/main.js

document.addEventListener('DOMContentLoaded', () => {
    const orderBtn = document.getElementById('btn-order');

    // Efecto simple al hacer clic
    orderBtn.addEventListener('click', () => {
        orderBtn.innerHTML = "¡Añadiendo al carrito! 🛒";
        orderBtn.classList.replace('bg-rappi', 'bg-carbon');
        
        setTimeout(() => {
            alert('¡Pronto recibirás tu deliciosa comida!');
            orderBtn.innerHTML = "Pedir ahora";
            orderBtn.classList.replace('bg-carbon', 'bg-rappi');
        }, 1000);
    });

    // Cambiar color del navbar al hacer scroll
    window.addEventListener('scroll', () => {
        const nav = document.querySelector('nav');
        if (window.scrollY > 50) {
            nav.classList.add('shadow-md', 'py-2');
            nav.classList.remove('py-4');
        } else {
            nav.classList.remove('shadow-md', 'py-2');
            nav.classList.add('py-4');
        }
    });
});