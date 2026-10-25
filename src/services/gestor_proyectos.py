"""
GestorProyectos — Lógica de negocio para la gestión de proyectos.

Métodos implementados (2 de 4):
  ✅ registrar_proyecto
  ✅ buscar_proyecto

Métodos pendientes de implementación:
  ❌ listar_proyectos
  ❌ validar_proyecto
"""

from __future__ import annotations

from src.models.proyecto import Proyecto
from src.services.excepciones import EntidadDuplicada, EntidadNoEncontrada, ReglaNegocioError
from src.services.persistencia_json import agregar_registro, buscar_registro, cargar_coleccion


class GestorProyectos:
    """Gestiona la creación, validación y consulta de proyectos."""

    # ------------------------------------------------------------------ #
    # Métodos IMPLEMENTADOS
    # ------------------------------------------------------------------ #

    def registrar_proyecto(self, id: str, nombre: str, descripcion: str) -> Proyecto:
        """
        Valida las reglas de negocio y registra un nuevo proyecto con
        estado inicial 'Activo'.

        Raises:
            ReglaNegocioError: si los datos no pasan las validaciones.
            EntidadDuplicada: si ya existe un proyecto con el mismo id.
        """
        # Validación inline (mientras validar_proyecto no esté implementado)
        if not id or not id.strip():
            raise ReglaNegocioError("El identificador del proyecto es obligatorio.")
        if not nombre or not nombre.strip():
            raise ReglaNegocioError("El nombre del proyecto es obligatorio.")
        if len(nombre) > 100:
            raise ReglaNegocioError("El nombre no puede superar los 100 caracteres.")
        if len(descripcion) > 500:
            raise ReglaNegocioError("La descripción no puede superar los 500 caracteres.")

        # Verificar unicidad
        existente = buscar_registro("proyectos", "id", id)
        if existente is not None:
            raise EntidadDuplicada("Proyecto", id)

        proyecto = Proyecto(id=id.strip(), nombre=nombre.strip(), descripcion=descripcion.strip())
        agregar_registro("proyectos", proyecto.to_dict())
        return proyecto

    def buscar_proyecto(self, id: str) -> Proyecto:
        """
        Busca un proyecto por su identificador.

        Raises:
            EntidadNoEncontrada: si el proyecto no existe.
        """
        registro = buscar_registro("proyectos", "id", id)
        if registro is None:
            raise EntidadNoEncontrada("Proyecto", id)
        return Proyecto.from_dict(registro)

    # ------------------------------------------------------------------ #
    # Métodos PENDIENTES de implementación
    # ------------------------------------------------------------------ #

    def listar_proyectos(self) -> list[Proyecto]:
        """
        Devuelve todos los proyectos registrados.

        TODO: Implementar — asignado a otro integrante del equipo.
        Debe cargar la colección 'proyectos' y reconstruir las entidades.
        """
        raise NotImplementedError(
            "listar_proyectos no implementado — pendiente de asignación."
        )

    def validar_proyecto(self, id: str, nombre: str, descripcion: str) -> None:
        """
        Comprueba todas las reglas de negocio de creación de un proyecto.

        TODO: Implementar — asignado a otro integrante del equipo.
        Debe validar: id no vacío y único, nombre obligatorio, longitud de
        descripción, formato del identificador según convenciones del proyecto.
        Lanza ReglaNegocioError o EntidadDuplicada según corresponda.
        """
        raise NotImplementedError(
            "validar_proyecto no implementado — pendiente de asignación."
        )
