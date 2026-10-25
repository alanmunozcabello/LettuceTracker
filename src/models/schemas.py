"""
Esquemas Pydantic para validación de solicitudes y respuestas HTTP.

Módulo MD0008 — Administración de Proyectos y Usuarios.
Separa los esquemas de creación (entrada) de los de respuesta (salida)
para que el cliente no pueda manipular campos controlados por el servidor.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from src.models.miembro_proyecto import ROLES_PERMITIDOS


# Esquemas de proyecto

class ProyectoCreate(BaseModel):
    """Esquema de entrada para crear un proyecto."""
    id: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Identificador único del proyecto.",
    )
    nombre: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre del proyecto.",
    )
    descripcion: str = Field(
        default="",
        max_length=500,
        description="Descripción del proyecto.",
    )

    model_config = {"extra": "forbid"}

    @field_validator("id")
    @classmethod
    def id_no_solo_espacios(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El identificador no puede estar compuesto solo por espacios.")
        return v.strip()

    @field_validator("nombre")
    @classmethod
    def nombre_no_solo_espacios(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar compuesto solo por espacios.")
        return v.strip()


class ProyectoResponse(BaseModel):
    """Esquema de salida para representar un proyecto."""
    id: str
    nombre: str
    descripcion: str
    estado: str
    fecha: str


# Esquemas de matrícula

class MatriculaCreate(BaseModel):
    """Esquema de entrada para registrar una matrícula."""
    id_usuario: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Identificador del usuario a matricular.",
    )
    id_curso: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Identificador del curso.",
    )

    model_config = {"extra": "forbid"}

    @field_validator("id_usuario")
    @classmethod
    def id_usuario_valido(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El id_usuario no puede estar vacío o ser solo espacios.")
        return v.strip()

    @field_validator("id_curso")
    @classmethod
    def id_curso_valido(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El id_curso no puede estar vacío o ser solo espacios.")
        return v.strip()


class MatriculaResponse(BaseModel):
    """Esquema de salida para representar una matrícula."""
    id_matricula: str
    id_usuario: str
    id_curso: str
    fecha: str


# Esquemas de miembros

class MiembroProyectoCreate(BaseModel):
    """Esquema de entrada para asignar un miembro a un proyecto."""
    id_usuario: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Identificador del usuario a asignar.",
    )
    rol: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Rol del usuario dentro del proyecto.",
    )

    model_config = {"extra": "forbid"}

    @field_validator("id_usuario")
    @classmethod
    def id_usuario_valido(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El id_usuario no puede estar vacío o ser solo espacios.")
        return v.strip()

    @field_validator("rol")
    @classmethod
    def rol_valido(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("El rol no puede estar vacío.")
        if v not in ROLES_PERMITIDOS:
            raise ValueError(
                f"Rol '{v}' no permitido. Roles válidos: {ROLES_PERMITIDOS}"
            )
        return v


class MiembroProyectoResponse(BaseModel):
    """Esquema de salida para representar la pertenencia a un proyecto."""
    id_miembro: str
    id_proyecto: str
    id_usuario: str
    rol: str


# Esquemas de permisos

class VerificarPermisoRequest(BaseModel):
    """Esquema de entrada para verificar si un usuario tiene un rol."""
    rol: str = Field(
        ...,
        min_length=1,
        description="El rol o permiso a verificar.",
    )

    model_config = {"extra": "forbid"}


class VerificarPermisoResponse(BaseModel):
    """Esquema de salida para el resultado de verificación de permiso."""
    id_proyecto: str
    id_usuario: str
    rol_solicitado: str
    tiene_permiso: bool
