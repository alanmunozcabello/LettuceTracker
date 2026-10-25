"""AdministracionFacade — Punto de entrada único de la capa de rutas al módulo MD0008."""

from __future__ import annotations

from src.models.matricula import Matricula
from src.models.miembro_proyecto import MiembroProyecto
from src.models.proyecto import Proyecto
from src.services.gestor_matricula import GestorMatricula
from src.services.gestor_permiso import GestorPermiso
from src.services.gestor_proyectos import GestorProyectos


class AdministracionFacade:
    """Fachada que orquesta los gestores del módulo MD0008."""

    def __init__(self) -> None:
        self._gestor_proyectos = GestorProyectos()
        self._gestor_matricula = GestorMatricula()
        self._gestor_permiso = GestorPermiso()

    def crear_proyecto(self, id: str, nombre: str, descripcion: str) -> Proyecto:
        """Crea un proyecto delegando en GestorProyectos."""
        return self._gestor_proyectos.registrar_proyecto(id, nombre, descripcion)

    def consultar_proyecto(self, id_proyecto: str) -> Proyecto:
        """Consulta un proyecto por su identificador."""
        return self._gestor_proyectos.buscar_proyecto(id_proyecto)

    def matricular_estudiante(self, id_usuario: str, id_curso: str) -> Matricula:
        """Registra la matrícula de un estudiante en un curso."""
        return self._gestor_matricula.registrar_matricula(id_usuario, id_curso)

    def asignar_permiso(self, id_proyecto: str, id_usuario: str, rol: str) -> tuple[MiembroProyecto, bool]:
        """Asigna un rol a un usuario en un proyecto. Devuelve (miembro, es_nuevo)."""
        return self._gestor_permiso.asignar_rol(id_proyecto, id_usuario, rol)

    def consultar_miembro(self, id_proyecto: str, id_usuario: str) -> MiembroProyecto:
        """Consulta la pertenencia de un usuario a un proyecto."""
        return self._gestor_permiso.buscar_miembro(id_proyecto, id_usuario)

    # Métodos pendientes de implementación

    def listar_proyectos(self) -> list[Proyecto]:
        """TODO: delegar en self._gestor_proyectos.listar_proyectos()."""
        raise NotImplementedError("listar_proyectos no implementado.")

    def consultar_matricula(self, id_matricula: str) -> Matricula:
        """TODO: delegar en self._gestor_matricula.buscar_matricula(id_matricula)."""
        raise NotImplementedError("consultar_matricula no implementado.")

    def listar_matriculas(self, id_usuario: str | None = None, id_curso: str | None = None) -> list[Matricula]:
        """TODO: delegar en self._gestor_matricula.listar_matriculas(id_usuario, id_curso)."""
        raise NotImplementedError("listar_matriculas no implementado.")

    def listar_miembros(self, id_proyecto: str) -> list[MiembroProyecto]:
        """TODO: delegar en self._gestor_permiso.listar_miembros(id_proyecto)."""
        raise NotImplementedError("listar_miembros no implementado.")

    def verificar_permiso(self, id_proyecto: str, id_usuario: str, rol: str) -> bool:
        """TODO: delegar en self._gestor_permiso.verificar_permiso(id_proyecto, id_usuario, rol)."""
        raise NotImplementedError("verificar_permiso no implementado.")
