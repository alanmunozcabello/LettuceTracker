"""
Modelo de dominio: Proyecto.

Representa un proyecto de desarrollo de software gestionado por LettuceTracker.
Los estados posibles están definidos en ESTADOS_PERMITIDOS. El estado inicial
al crear un proyecto es siempre 'Activo'.
"""

from __future__ import annotations

from datetime import datetime
from typing import ClassVar


# --- Estados permitidos para un proyecto ---
# Decisión provisional: estos estados se definen aquí porque el repositorio
# no contenía una lista preexistente. Si el proyecto define estados en otra
# parte, esta lista debe unificarse con aquella.
ESTADOS_PERMITIDOS: list[str] = ["Activo", "Inactivo", "Finalizado", "Cancelado"]


class Proyecto:
    """Entidad de dominio que representa un proyecto."""

    ESTADOS_PERMITIDOS: ClassVar[list[str]] = ESTADOS_PERMITIDOS

    def __init__(self, id: str, nombre: str, descripcion: str) -> None:
        self.id: str = id
        self.nombre: str = nombre
        self.descripcion: str = descripcion
        self.estado: str = "Activo"
        self.fecha: str = datetime.now().isoformat()

    # --- Métodos de dominio ---

    def set_estado(self, estado: str) -> None:
        """Cambia el estado del proyecto si el nuevo estado es permitido."""
        if estado not in ESTADOS_PERMITIDOS:
            raise ValueError(
                f"Estado '{estado}' no permitido. "
                f"Estados válidos: {ESTADOS_PERMITIDOS}"
            )
        self.estado = estado

    def get_nombre(self) -> str:
        """Devuelve el nombre del proyecto."""
        return self.nombre

    def to_dict(self) -> dict:
        """Serializa el proyecto a diccionario para persistencia JSON."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "fecha": self.fecha,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Proyecto":
        """Reconstruye un Proyecto a partir de un diccionario."""
        proyecto = cls(
            id=data["id"],
            nombre=data["nombre"],
            descripcion=data["descripcion"],
        )
        proyecto.estado = data.get("estado", "Activo")
        proyecto.fecha = data.get("fecha", datetime.now().isoformat())
        return proyecto
