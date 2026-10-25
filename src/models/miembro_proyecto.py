"""
Modelo de dominio: MiembroProyecto.

Representa la pertenencia de un usuario a un proyecto con un rol específico.
El rol es por relación (usuario ↔ proyecto), no global del sistema.

NOTA — Roles permitidos:
Los roles se extrajeron del dashboard existente del proyecto: Líder de Proyecto,
Desarrollador, Tester, Arquitecto. Se agregó 'Documentador' como rol adicional
común en equipos de desarrollo. Esta lista se define en ROLES_PERMITIDOS y es
el único punto de configuración. Si el proyecto define roles en otra parte,
deben unificarse aquí.
"""

from __future__ import annotations

from typing import ClassVar


# Roles permitidos dentro de un proyecto
ROLES_PERMITIDOS: list[str] = [
    "Líder de Proyecto",
    "Desarrollador",
    "Tester",
    "Arquitecto",
    "Documentador",
]


class MiembroProyecto:
    """Entidad de dominio que relaciona un usuario con un proyecto y su rol."""

    ROLES_PERMITIDOS: ClassVar[list[str]] = ROLES_PERMITIDOS

    def __init__(
        self, id_miembro: str, id_proyecto: str, id_usuario: str, rol: str
    ) -> None:
        self.id_miembro: str = id_miembro
        self.id_proyecto: str = id_proyecto
        self.id_usuario: str = id_usuario
        self.rol: str = rol

    def get_rol(self) -> str:
        """Devuelve el rol del miembro en el proyecto."""
        return self.rol

    def to_dict(self) -> dict:
        """Serializa el miembro para persistencia JSON."""
        return {
            "id_miembro": self.id_miembro,
            "id_proyecto": self.id_proyecto,
            "id_usuario": self.id_usuario,
            "rol": self.rol,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MiembroProyecto":
        """Reconstruye un MiembroProyecto a partir de un diccionario."""
        return cls(
            id_miembro=data["id_miembro"],
            id_proyecto=data["id_proyecto"],
            id_usuario=data["id_usuario"],
            rol=data["rol"],
        )
