"""Autenticación básica contra la colección JSON de usuarios."""

from __future__ import annotations

import hmac
import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from src.services.persistencia_json import cargar_coleccion

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 4
JWT_COOKIE_NAME = "lettuce_access_token"
JWT_SECRET = os.getenv(
    "LETTUCE_JWT_SECRET",
    "dev-only-change-this-secret-before-deployment",
)


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


def crear_token_acceso(usuario: dict[str, Any]) -> str:
    """Crea un JWT de acceso con una duración máxima de cuatro horas."""
    ahora = datetime.now(timezone.utc)
    payload = {
        "sub": str(usuario["id"]),
        "email": str(usuario["email"]),
        "iat": ahora,
        "exp": ahora + timedelta(hours=JWT_EXPIRATION_HOURS),
        "jti": uuid.uuid4().hex,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def validar_token_acceso(token: str) -> dict[str, Any]:
    """Valida firma y expiración del JWT y devuelve sus claims."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.InvalidTokenError as exc:
        raise CredencialesInvalidas from exc
