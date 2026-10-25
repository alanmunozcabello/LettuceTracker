"""
Modelo de dominio: Matricula.

Representa la inscripción de un estudiante (usuario) en un curso.

NOTA — Dependencia no verificable:
El repositorio actual no posee una entidad de Curso ni un sistema de usuarios
con persistencia. Por lo tanto, la verificación de existencia de usuario y
curso se realiza contra los datos almacenados en los archivos JSON provisionales.
Cuando exista un módulo de Cursos y de Usuarios, las validaciones deben
delegarse a esos módulos.
"""

from __future__ import annotations

from datetime import datetime


class Matricula:
    """Entidad de dominio que representa la matrícula de un usuario en un curso."""

    def __init__(self, id_matricula: str, id_usuario: str, id_curso: str) -> None:
        self.id_matricula: str = id_matricula
        self.id_usuario: str = id_usuario
        self.id_curso: str = id_curso
        self.fecha: str = datetime.now().isoformat()

    def get_detalles(self) -> dict:
        """Devuelve los detalles de la matrícula como diccionario."""
        return {
            "id_matricula": self.id_matricula,
            "id_usuario": self.id_usuario,
            "id_curso": self.id_curso,
            "fecha": self.fecha,
        }

    def to_dict(self) -> dict:
        """Serializa la matrícula para persistencia JSON."""
        return self.get_detalles()

    @classmethod
    def from_dict(cls, data: dict) -> "Matricula":
        """Reconstruye una Matricula a partir de un diccionario."""
        matricula = cls(
            id_matricula=data["id_matricula"],
            id_usuario=data["id_usuario"],
            id_curso=data["id_curso"],
        )
        matricula.fecha = data.get("fecha", datetime.now().isoformat())
        return matricula
