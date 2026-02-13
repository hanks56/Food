# Guía del proyecto — App de comidas a domicilio (estilo Rappi/Didi)

## Cómo funciona una app de domicilio en línea

En apps como Rappi, Didi Food o Uber Eats hay **tres actores** y un flujo claro:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CLIENTE   │────▶│   TIENDA/   │────▶│   PEDIDO    │
│  (usuario)  │     │  RESTAURANTE│     │  (orden)    │
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │                    │
       │ 1. Busca/elige      │ 2. Recibe pedido   │ 3. Entrega
       │ 2. Añade al carrito │    y prepara       │    (reparto)
       │ 3. Paga / confirma  │                    │
       └────────────────────┴────────────────────┘
```

**Flujo mínimo que necesitas:**

1. **Cliente** se registra / inicia sesión.
2. **Cliente** ve **catálogo** (tiendas o categorías) y **productos**.
3. **Cliente** añade productos al **carrito**.
4. **Cliente** confirma y crea una **orden (pedido)**.
5. (Opcional más adelante) Estado del pedido, reparto, etc.

Tu stack (Python, Django, Jinja, SQL) encaja perfecto para este flujo.

---

## Módulos importantes — Checklist

| Módulo                            | ¿Lo tienes?                                       | Descripción breve |
|--------                           |-------------                                      |-------------------|
| **Usuarios** (registro + login)   | ✅ App `users` (falta implementar vistas/modelo)  | Registro, login, logout, perfil básico |
| **Productos / Catálogo**          | ✅ App `store` (modelos vacíos)                   | Categorías, productos, precios, tiendas o “restaurantes” |
| **Carrito**                       | ✅ App `cart` (modelos vacíos)                    | Items en carrito por usuario/sesión |
| **Órdenes (pedidos)**             | ✅ App `orders` (modelos vacíos)                  | Pedido = carrito confirmado con estado, dirección, etc. |
| **Home / Landing**                | ✅ Funcionando                                    | Página de entrada, enlaces a login/registro |
| **Direcciones**                   | ⚠️ Opcional ahora | Para envío; se puede añadir en Fase 2 |
| **Pagos**                         | ⚠️ Opcional ahora | Integración pasarela; mejor después del MVP |

**¿Se te está olvidando algo para el MVP?**

- **Sesiones / autenticación:** ya usas Django (auth), solo falta conectar login/registro.
- **Protección de rutas:** que “carrito” y “orden” solo los vea quien esté logueado.
- **Un “restaurante” o “tienda”:** en Rappi/Didi hay tiendas; cada producto suele pertenecer a una tienda. Conviene tener aunque sea un modelo `Store` o `Restaurant` y que `Product` tenga `ForeignKey` a él.

Resumen: con **usuarios, productos/catálogo, carrito y órdenes** tienes el núcleo. Direcciones y pagos los puedes dejar para después.

---

## Tu estructura actual (resumen)

```
food/
├── config/           # Settings, urls principales
├── applications/
│   ├── home/         # Landing ✅
│   ├── users/        # URLs de register/login ✅, vistas vacías ❌, modelos vacíos ❌
│   ├── store/        # Catálogo/productos — modelos vacíos ❌
│   ├── cart/         # Carrito — modelos vacíos ❌
│   └── orders/       # Pedidos — modelos vacíos ❌
└── templates/
```

**Problemas detectados:**

1. En `config/urls.py` **no está incluida** la app `users` (tienes solo `home`).
2. Las vistas de `users` están vacías (solo el placeholder).
3. Todos los modelos de `store`, `cart`, `orders` y `users` están vacíos.
4. Falta configurar `AUTH_USER_MODEL` si quieres usuario personalizado, y `LOGIN_REDIRECT_URL` / `LOGOUT_REDIRECT_URL`.

---

## Cómo modularizar y optimizar

**Principio:** cada app con una responsabilidad clara y pocas dependencias.

| App | Responsabilidad | Depende de |
|-----|-----------------|------------|
| **users** | Registro, login, logout, perfil (y luego dirección si quieres) | Ninguna (solo Django auth) |
| **store** | Tiendas/restaurantes, categorías, productos | Ninguna |
| **cart** | Carrito (ítems: producto + cantidad) | `store` (Product), `users` (User) o sesión |
| **orders** | Pedido (cabecera + líneas), estado | `store`, `users`, opcionalmente `cart` |

**Buenas prácticas para que sea optimizable:**

1. **URLs por app:** cada app con su `urls.py` y en `config/urls.py` solo `include()` (ya lo tienes en home; falta users, store, cart, orders).
2. **Nombres de URLs con `app_name`:** para usar `{% url 'users_app:user-login' %}` y no acoplarte a rutas fijas.
3. **Templates por app:** por ejemplo `templates/users/`, `templates/store/`, `templates/cart/`, `templates/orders/`. En `settings.py` pon `DIRS`: `[BASE_DIR / 'templates']` y que cada app pueda usar su subcarpeta.
4. **Modelos en la app correcta:** dirección de envío puede estar en `users` (UserAddress) o en `orders` (Address en el pedido). Para empezar, una dirección simple en el pedido basta.
5. **No duplicar lógica:** carrito y órdenes son distintos: carrito = “borrador”; orden = “confirmado”. Al confirmar, creas la orden a partir del carrito y luego puedes vaciar el carrito.

---

## Orden recomendado (por dónde empezar)

Para no complicarte y ser eficaz:

1. **Semana 1 — Base y usuarios**
   - Definir modelo de usuario (o usar `User` de Django).
   - Implementar registro e inicio de sesión en `users` (vistas + formularios + templates).
   - Incluir `users` en `config/urls.py` y enlazar Login/Registro desde `base.html`.
   - Opcional: logout y vista “mi cuenta”.

2. **Semana 2 — Catálogo y carrito**
   - En `store`: modelos `Category`, `Store` (o Restaurant), `Product` (nombre, precio, tienda, categoría).
   - Vistas y templates: listar tiendas/categorías y listar productos (por tienda o por categoría).
   - En `cart`: modelo `Cart` / `CartItem` (usuario o sesión, producto, cantidad). Vistas: añadir, ver carrito, actualizar cantidad, quitar ítem.
   - Incluir URLs de `store` y `cart` en `config/urls.py`.

3. **Semana 3 — Órdenes y cierre**
   - En `orders`: modelos `Order` (usuario, fecha, estado, total, dirección de envío) y `OrderItem` (producto, cantidad, precio).
   - Flujo: “Confirmar pedido” toma el carrito actual, crea `Order` + `OrderItem`, vacía el carrito, redirige a “gracias” o “mis pedidos”.
   - Vista “Mis pedidos” (lista de órdenes del usuario).
   - Ajustes finales: permisos (solo logueados en carrito/orden), mensajes de éxito/error, algo de estilo en templates.

---

## Roadmap de 3 semanas (resumen)

| Semana | Entregable |
|--------|------------|
| **1** | Registro, login, logout; rutas y navegación; usuario listo para usar en el resto de la app. |
| **2** | Catálogo (tiendas + productos); carrito (añadir, ver, editar, vaciar). |
| **3** | Crear orden desde carrito; pantalla “Mis pedidos”; flujo mínimo completo. |

Después de eso puedes sumar: direcciones guardadas, estados de pedido (recibido, en preparación, enviado), pagos, etc.

---

## ¿Qué más debería saber de tu proyecto?

Para afinar la guía y el orden de tareas, ayuda saber:

1. **Usuario:** ¿solo clientes o también dueños de tienda/restaurante? (Para el MVP suele bastar solo clientes.)
2. **Productos:** ¿una sola “tienda” global o varias tiendas/restaurantes desde el día 1?
3. **Carrito:** ¿un carrito por usuario (logrado) o también carrito anónimo (por sesión) antes de login?
4. **Pagos:** ¿solo “pago contra entrega” por ahora o quieres integrar pasarela (Stripe, Mercado Pago, etc.) en estas 3 semanas?
5. **Diseño:** ¿quieres mantener solo Tailwind en base.html o añadir más páginas con el mismo estilo (FastBites)?
6. **Despliegue:** ¿solo local o tienes previsto subir a un servidor (Render, Railway, etc.)?

Cuando me digas estas cosas, puedo bajar al detalle: modelos concretos (campos), vistas y nombres de URLs, y orden exacto de tareas semana a semana. Si quieres, el siguiente paso puede ser: **conectar `users` en `config/urls.py` y esbozar los modelos de `users` y `store`** para que puedas empezar la Semana 1 con pasos concretos.
