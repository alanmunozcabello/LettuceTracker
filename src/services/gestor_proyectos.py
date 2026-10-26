"""GestorProyectos — Lógica de negocio para la gestión de proyectos."""

from __future__ import annotations

from src.models.proyecto import Proyecto
from src.services.excepciones import EntidadDuplicada, EntidadNoEncontrada, ReglaNegocioError
from src.services.persistencia_json import agregar_registro, buscar_registro, cargar_coleccion


class GestorProyectos:
    """Gestiona la creación, validación y consulta de proyectos."""

    def registrar_proyecto(self, id: str, nombre: str, descripcion: str) -> Proyecto:
        """Valida y registra un nuevo proyecto con estado inicial 'Activo'."""
        if not id or not id.strip():
            raise ReglaNegocioError("El identificador del proyecto es obligatorio.")
        if not nombre or not nombre.strip():
            raise ReglaNegocioError("El nombre del proyecto es obligatorio.")
        if len(nombre) > 100:
            raise ReglaNegocioError("El nombre no puede superar los 100 caracteres.")
        if len(descripcion) > 500:
            raise ReglaNegocioError("La descripción no puede superar los 500 caracteres.")

        existente = buscar_registro("proyectos", "id", id)
        if existente is not None:
            raise EntidadDuplicada("Proyecto", id)

        proyecto = Proyecto(id=id.strip(), nombre=nombre.strip(), descripcion=descripcion.strip())
        agregar_registro("proyectos", proyecto.to_dict())
        return proyecto

    def buscar_proyecto(self, id: str) -> Proyecto:
        """Busca un proyecto por su identificador."""
        registro = buscar_registro("proyectos", "id", id)
        if registro is None:
            raise EntidadNoEncontrada("Proyecto", id)
        return Proyecto.from_dict(registro)

    def listar_proyectos(self) -> list[Proyecto]:
        """Devuelve todos los proyectos registrados."""
        return [
            Proyecto.from_dict(registro)
            for registro in cargar_coleccion("proyectos")
        ]

    def validar_proyecto(self, id: str, nombre: str, descripcion: str) -> None:
        """Método pendiente de implementación."""
        raise NotImplementedError("validar_proyecto no implementado.")
