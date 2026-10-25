"""
AdministracionFacade — Punto de entrada único de la capa de rutas
al módulo MD0008.

Las rutas SIEMPRE deben invocar métodos de esta clase; no deben llamar
directamente a los gestores.

Métodos implementados (5 de 10):
  ✅ crear_proyecto
  ✅ consultar_proyecto
  ✅ matricular_estudiante
  ✅ asignar_permiso
  ✅ consultar_miembro

Métodos pendientes de implementación:
  ❌ listar_proyectos
  ❌ consultar_matricula
  ❌ listar_matriculas
  ❌ listar_miembros
  ❌ verificar_permiso
"""

from __future__ import annotations

from src.models.matricula import Matricula
from src.models.miembro_proyecto import MiembroProyecto
from src.models.proyecto import Proyecto
from src.services.gestor_matricula import GestorMatricula
from src.services.gestor_permiso import GestorPermiso
from src.services.gestor_proyectos import GestorProyectos


class AdministracionFacade:
    """
    Fachada que orquesta los gestores del módulo MD0008.

    Cada método delega en el gestor correspondiente, manteniendo
    la separación de responsabilidades.
    """

    def __init__(self) -> None:
        self._gestor_proyectos = GestorProyectos()
        self._gestor_matricula = GestorMatricula()
        self._gestor_permiso = GestorPermiso()

    # ------------------------------------------------------------------ #
    # Métodos IMPLEMENTADOS
    # ------------------------------------------------------------------ #

    def crear_proyecto(
        self, id: str, nombre: str, descripcion: str
    ) -> Proyecto:
        """Crea un proyecto delegando en GestorProyectos."""
        return self._gestor_proyectos.registrar_proyecto(id, nombre, descripcion)

    def consultar_proyecto(self, id_proyecto: str) -> Proyecto:
        """Consulta un proyecto por su identificador."""
        return self._gestor_proyectos.buscar_proyecto(id_proyecto)

    def matricular_estudiante(
        self, id_usuario: str, id_curso: str
    ) -> Matricula:
        """Registra la matrícula de un estudiante en un curso."""
        return self._gestor_matricula.registrar_matricula(id_usuario, id_curso)

    def asignar_permiso(
        self, id_proyecto: str, id_usuario: str, rol: str
    ) -> tuple[MiembroProyecto, bool]:
        """
        Asigna un rol a un usuario en un proyecto.

        Devuelve (miembro, es_nuevo) donde es_nuevo indica si se creó
        la pertenencia (True) o se actualizó una existente (False).
        """
        return self._gestor_permiso.asignar_rol(id_proyecto, id_usuario, rol)

    def consultar_miembro(
        self, id_proyecto: str, id_usuario: str
    ) -> MiembroProyecto:
        """Consulta la pertenencia de un usuario a un proyecto."""
        return self._gestor_permiso.buscar_miembro(id_proyecto, id_usuario)

    # ------------------------------------------------------------------ #
    # Métodos PENDIENTES de implementación
    # ------------------------------------------------------------------ #

    def listar_proyectos(self) -> list[Proyecto]:
        """
        Lista todos los proyectos registrados.

        TODO: Implementar — asignado a otro integrante del equipo.
        Debe delegar en self._gestor_proyectos.listar_proyectos().
        """
        raise NotImplementedError(
            "listar_proyectos no implementado — pendiente de asignación."
        )

    def consultar_matricula(self, id_matricula: str) -> Matricula:
        """
        Consulta una matrícula por su identificador.

        TODO: Implementar — asignado a otro integrante del equipo.
        Debe delegar en self._gestor_matricula.buscar_matricula(id_matricula).
        """
        raise NotImplementedError(
            "consultar_matricula no implementado — pendiente de asignación."
        )

    def listar_matriculas(
        self, id_usuario: str | None = None, id_curso: str | None = None
    ) -> list[Matricula]:
        """
        Lista matrículas con filtros opcionales.

        TODO: Implementar — asignado a otro integrante del equipo.
        Debe delegar en self._gestor_matricula.listar_matriculas(id_usuario, id_curso).
        """
        raise NotImplementedError(
            "listar_matriculas no implementado — pendiente de asignación."
        )

    def listar_miembros(self, id_proyecto: str) -> list[MiembroProyecto]:
        """
        Lista los miembros de un proyecto.

        TODO: Implementar — asignado a otro integrante del equipo.
        Debe delegar en self._gestor_permiso.listar_miembros(id_proyecto).
        """
        raise NotImplementedError(
            "listar_miembros no implementado — pendiente de asignación."
        )

    def verificar_permiso(
        self, id_proyecto: str, id_usuario: str, rol: str
    ) -> bool:
        """
        Verifica si un usuario tiene un rol en un proyecto.

        TODO: Implementar — asignado a otro integrante del equipo.
        Debe delegar en self._gestor_permiso.verificar_permiso(id_proyecto, id_usuario, rol).
        """
        raise NotImplementedError(
            "verificar_permiso no implementado — pendiente de asignación."
        )
