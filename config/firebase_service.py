"""
Servicio para sincronizar datos con Firebase Realtime Database.
Usa la REST API de Firebase (requests).
"""
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def _get_base_url():
    """Obtiene la URL base de Firebase, asegurando que termine en .json cuando se use."""
    url = getattr(settings, "FIREBASE_DATABASE_URL", "") or ""
    if not url:
        return None
    return url.rstrip("/")


def sync_user_to_firebase(user_id: int, email: str, first_name: str, last_name: str) -> bool:
    """
    Sincroniza los datos del usuario a Firebase Realtime Database.
    NO guarda la contraseña (seguridad).
    Devuelve True si se guardó correctamente, False en caso contrario.
    """
    base_url = _get_base_url()
    if not base_url:
        logger.warning("FIREBASE_DATABASE_URL no configurada. Omitiendo sync a Firebase.")
        return False

    path = f"users/{user_id}.json"
    url = f"{base_url}/{path}"
    secret = getattr(settings, "FIREBASE_DATABASE_SECRET", "") or ""
    if secret:
        url += f"?auth={secret}"

    data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "username": f"{first_name} {last_name}".strip() or email,
    }

    try:
        resp = requests.put(url, json=data, timeout=10)
        if resp.status_code in (200, 204):
            return True
        logger.error("Firebase sync falló: %s - %s", resp.status_code, resp.text[:200])
        return False
    except Exception as e:
        logger.exception("Error al sincronizar con Firebase: %s", e)
        return False


def get_user_from_firebase(user_id: int) -> dict | None:
    """
    Obtiene los datos del usuario desde Firebase (opcional, para futuras funciones).
    """
    base_url = _get_base_url()
    if not base_url:
        return None

    path = f"users/{user_id}.json"
    url = f"{base_url}/{path}"
    secret = getattr(settings, "FIREBASE_DATABASE_SECRET", "") or ""
    if secret:
        url += f"?auth={secret}"

    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception as e:
        logger.exception("Error al leer de Firebase: %s", e)
        return None
