"""Rutas HTTP del login provisional."""

from __future__ import annotations

from fastapi import APIRouter, Cookie, HTTPException, Response, status
from fastapi.responses import FileResponse

from src.models.schemas import LoginRequest, LoginResponse, SesionResponse
from src.services.autenticacion import (
    JWT_COOKIE_NAME,
    JWT_EXPIRATION_HOURS,
    CredencialesInvalidas,
    autenticar_usuario,
    crear_token_acceso,
    validar_token_acceso,
)
from src.services.persistencia_json import buscar_registro

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])


@router.post("/login", response_model=LoginResponse, summary="Iniciar sesión")
def iniciar_sesion(datos: LoginRequest) -> Response:
    """Valida correo y contraseña contra los usuarios registrados en JSON."""
    try:
        usuario = autenticar_usuario(datos.email, datos.contrasena)
    except CredencialesInvalidas:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
        )

    token = crear_token_acceso(usuario)
    response = Response(
        content=LoginResponse(autenticado=True, usuario=usuario).model_dump_json(),
        media_type="application/json",
    )
    response.set_cookie(
        key=JWT_COOKIE_NAME,
        value=token,
        max_age=JWT_EXPIRATION_HOURS * 60 * 60,
        httponly=True,
        samesite="lax",
        path="/",
    )
    return response


def _usuario_de_token(token: str | None) -> dict[str, str | None]:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La sesión no está autenticada.",
        )
    try:
        claims = validar_token_acceso(token)
    except CredencialesInvalidas:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La sesión expiró o no es válida.",
        )

    usuario = buscar_registro("usuarios", "id", str(claims.get("sub")))
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El usuario de la sesión ya no existe.",
        )
    return {
        "id": usuario.get("id"),
        "nombre": usuario.get("nombre"),
        "email": usuario.get("email"),
    }


@router.get("/me", response_model=SesionResponse, summary="Validar sesión")
def validar_sesion(
    token: str | None = Cookie(default=None, alias=JWT_COOKIE_NAME),
) -> SesionResponse:
    """Comprueba que la cookie JWT siga vigente."""
    return SesionResponse(autenticado=True, usuario=_usuario_de_token(token))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, summary="Cerrar sesión")
def cerrar_sesion(response: Response) -> Response:
    """Elimina la cookie de autenticación del navegador."""
    response.delete_cookie(key=JWT_COOKIE_NAME, path="/")
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/dashboard", include_in_schema=False)
def dashboard_protegido(
    token: str | None = Cookie(default=None, alias=JWT_COOKIE_NAME),
) -> FileResponse:
    """Sirve el dashboard solo a sesiones con un JWT válido."""
    _usuario_de_token(token)
    return FileResponse(
        "src/static/html/dashboard.html",
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
    )
