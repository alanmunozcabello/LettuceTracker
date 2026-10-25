"""GestorPermiso — Lógica de negocio para la gestión de miembros y roles."""

from __future__ import annotations

import uuid

from src.models.miembro_proyecto import ROLES_PERMITIDOS, MiembroProyecto
from src.services.excepciones import EntidadDuplicada, EntidadNoEncontrada, ReglaNegocioError
from src.services.persistencia_json import agregar_registro, buscar_registro, buscar_registros, actualizar_registro


class GestorPermiso:
    """Gestiona la asignación de roles y permisos de miembros dentro de proyectos."""

    def asignar_rol(self, id_proyecto: str, id_usuario: str, rol: str) -> tuple[MiembroProyecto, bool]:
        """Asigna un rol a un usuario en un proyecto. Devuelve (miembro, es_nuevo)."""
        proyecto = buscar_registro("proyectos", "id", id_proyecto)
        if proyecto is None:
            raise EntidadNoEncontrada("Proyecto", id_proyecto)

        usuario = buscar_registro("usuarios", "id", id_usuario)
        if usuario is None:
            raise EntidadNoEncontrada("Usuario", id_usuario)

        if rol not in ROLES_PERMITIDOS:
            raise ReglaNegocioError(f"Rol '{rol}' no permitido. Roles válidos: {ROLES_PERMITIDOS}")

        miembros = buscar_registros("miembros", filtros={"id_proyecto": id_proyecto, "id_usuario": id_usuario})

        if miembros:
            miembro_existente = miembros[0]
            miembro_existente["rol"] = rol
            actualizar_registro("miembros", "id_miembro", miembro_existente["id_miembro"], {"rol": rol})
            return MiembroProyecto.from_dict(miembro_existente), False

        id_miembro = f"MBR-{uuid.uuid4().hex[:8].upper()}"
        miembro = MiembroProyecto(id_miembro=id_miembro, id_proyecto=id_proyecto, id_usuario=id_usuario, rol=rol)
        agregar_registro("miembros", miembro.to_dict())
        return miembro, True

    def buscar_miembro(self, id_proyecto: str, id_usuario: str) -> MiembroProyecto:
        """Localiza la pertenencia de un usuario a un proyecto."""
        proyecto = buscar_registro("proyectos", "id", id_proyecto)
        if proyecto is None:
            raise EntidadNoEncontrada("Proyecto", id_proyecto)

        miembros = buscar_registros("miembros", filtros={"id_proyecto": id_proyecto, "id_usuario": id_usuario})
        if not miembros:
            raise EntidadNoEncontrada("Miembro", f"proyecto={id_proyecto}, usuario={id_usuario}")
        return MiembroProyecto.from_dict(miembros[0])

    def verificar_permiso(self, id_proyecto: str, id_usuario: str, rol: str) -> bool:
        """Método pendiente de implementación."""
        raise NotImplementedError("verificar_permiso no implementado.")

    def listar_miembros(self, id_proyecto: str) -> list[MiembroProyecto]:
        """Método pendiente de implementación."""
        raise NotImplementedError("listar_miembros no implementado.")
