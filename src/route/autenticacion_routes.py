"""Rutas HTTP del login provisional."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from src.models.schemas import LoginRequest, LoginResponse
from src.services.autenticacion import CredencialesInvalidas, autenticar_usuario

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])


@router.post("/login", response_model=LoginResponse, summary="Iniciar sesión")
def iniciar_sesion(datos: LoginRequest) -> LoginResponse:
    """Valida correo y contraseña contra los usuarios registrados en JSON."""
    try:
        usuario = autenticar_usuario(datos.email, datos.contrasena)
    except CredencialesInvalidas:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
        )

    return LoginResponse(autenticado=True, usuario=usuario)
