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

    def listar_proyectos(self) -> list[Proyecto]:
        """Método pendiente de implementación."""
        raise NotImplementedError("listar_proyectos no implementado.")

    def consultar_matricula(self, id_matricula: str) -> Matricula:
        """Método pendiente de implementación."""
        raise NotImplementedError("consultar_matricula no implementado.")

    def listar_matriculas(self, id_usuario: str | None = None, id_curso: str | None = None) -> list[Matricula]:
        """Método pendiente de implementación."""
        raise NotImplementedError("listar_matriculas no implementado.")

    def listar_miembros(self, id_proyecto: str) -> list[MiembroProyecto]:
        """Método pendiente de implementación."""
        raise NotImplementedError("listar_miembros no implementado.")

    def verificar_permiso(self, id_proyecto: str, id_usuario: str, rol: str) -> bool:
        """Método pendiente de implementación."""
        raise NotImplementedError("verificar_permiso no implementado.")
