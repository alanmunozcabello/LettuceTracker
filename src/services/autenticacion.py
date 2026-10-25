"""Autenticación básica contra la colección JSON de usuarios."""

from __future__ import annotations

import hmac
from typing import Any

from src.services.persistencia_json import cargar_coleccion


class CredencialesInvalidas(Exception):
    """Indica que el correo o la contraseña no coinciden con un usuario."""


def autenticar_usuario(email: str, contrasena: str) -> dict[str, Any]:
    """
    Devuelve los datos públicos del usuario si sus credenciales coinciden.

    La contraseña se compara en texto plano únicamente por tratarse de una
    implementación provisional. Nunca se incluye en el resultado.
    """
    email_normalizado = email.strip().casefold()

    for usuario in cargar_coleccion("usuarios"):
        email_usuario = str(usuario.get("email", "")).strip().casefold()
        contrasena_usuario = str(usuario.get("contrasena", ""))
        if hmac.compare_digest(email_usuario, email_normalizado) and hmac.compare_digest(
            contrasena_usuario, contrasena
        ):
            return {
                "id": usuario.get("id"),
                "nombre": usuario.get("nombre"),
                "email": usuario.get("email"),
            }

    raise CredencialesInvalidas
