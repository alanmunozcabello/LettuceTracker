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

    # Métodos pendientes de implementación

    def listar_proyectos(self) -> list[Proyecto]:
        """TODO: cargar colección 'proyectos' y reconstruir las entidades."""
        raise NotImplementedError("listar_proyectos no implementado.")

    def validar_proyecto(self, id: str, nombre: str, descripcion: str) -> None:
        """TODO: validar reglas de negocio de creación (id único, nombre obligatorio, longitud)."""
        raise NotImplementedError("validar_proyecto no implementado.")
