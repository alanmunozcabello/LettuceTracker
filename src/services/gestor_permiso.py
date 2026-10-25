"""
GestorPermiso — Lógica de negocio para la gestión de miembros y roles.

Métodos implementados (2 de 4):
  ✅ asignar_rol
  ✅ buscar_miembro

Métodos pendientes de implementación:
  ❌ verificar_permiso
  ❌ listar_miembros
"""

from __future__ import annotations

import uuid

from src.models.miembro_proyecto import ROLES_PERMITIDOS, MiembroProyecto
from src.services.excepciones import EntidadDuplicada, EntidadNoEncontrada, ReglaNegocioError
from src.services.persistencia_json import (
    agregar_registro,
    buscar_registro,
    buscar_registros,
    actualizar_registro,
)


class GestorPermiso:
    """Gestiona la asignación de roles y permisos de miembros dentro de proyectos."""

    # ------------------------------------------------------------------ #
    # Métodos IMPLEMENTADOS
    # ------------------------------------------------------------------ #

    def asignar_rol(
        self, id_proyecto: str, id_usuario: str, rol: str
    ) -> tuple[MiembroProyecto, bool]:
        """
        Asigna un rol a un usuario dentro de un proyecto.

        Si el usuario ya es miembro del proyecto, actualiza su rol y
        devuelve (miembro, False) indicando que fue actualización.
        Si no era miembro, crea la pertenencia y devuelve (miembro, True)
        indicando que fue creación.

        Raises:
            EntidadNoEncontrada: si el proyecto o el usuario no existen.
            ReglaNegocioError: si el rol no es válido.
        """
        # Validar que el proyecto exista
        proyecto = buscar_registro("proyectos", "id", id_proyecto)
        if proyecto is None:
            raise EntidadNoEncontrada("Proyecto", id_proyecto)

        # Validar que el usuario exista
        usuario = buscar_registro("usuarios", "id", id_usuario)
        if usuario is None:
            raise EntidadNoEncontrada("Usuario", id_usuario)

        # Validar rol
        if rol not in ROLES_PERMITIDOS:
            raise ReglaNegocioError(
                f"Rol '{rol}' no permitido. Roles válidos: {ROLES_PERMITIDOS}"
            )

        # Verificar si ya es miembro del proyecto
        miembros = buscar_registros(
            "miembros",
            filtros={"id_proyecto": id_proyecto, "id_usuario": id_usuario},
        )

        if miembros:
            # Actualizar rol existente
            miembro_existente = miembros[0]
            miembro_existente["rol"] = rol
            actualizar_registro(
                "miembros", "id_miembro", miembro_existente["id_miembro"],
                {"rol": rol},
            )
            return MiembroProyecto.from_dict(miembro_existente), False

        # Crear nueva pertenencia
        id_miembro = f"MBR-{uuid.uuid4().hex[:8].upper()}"
        miembro = MiembroProyecto(
            id_miembro=id_miembro,
            id_proyecto=id_proyecto,
            id_usuario=id_usuario,
            rol=rol,
        )
        agregar_registro("miembros", miembro.to_dict())
        return miembro, True

    def buscar_miembro(
        self, id_proyecto: str, id_usuario: str
    ) -> MiembroProyecto:
        """
        Localiza la pertenencia de un usuario a un proyecto.

        Raises:
            EntidadNoEncontrada: si el proyecto no existe o el usuario
                                  no es miembro del proyecto.
        """
        # Validar que el proyecto exista
        proyecto = buscar_registro("proyectos", "id", id_proyecto)
        if proyecto is None:
            raise EntidadNoEncontrada("Proyecto", id_proyecto)

        miembros = buscar_registros(
            "miembros",
            filtros={"id_proyecto": id_proyecto, "id_usuario": id_usuario},
        )
        if not miembros:
            raise EntidadNoEncontrada(
                "Miembro",
                f"proyecto={id_proyecto}, usuario={id_usuario}",
            )
        return MiembroProyecto.from_dict(miembros[0])

    # ------------------------------------------------------------------ #
    # Métodos PENDIENTES de implementación
    # ------------------------------------------------------------------ #

    def verificar_permiso(
        self, id_proyecto: str, id_usuario: str, rol: str
    ) -> bool:
        """
        Comprueba si el usuario tiene el rol solicitado en el proyecto.

        TODO: Implementar — asignado a otro integrante del equipo.
        Debe buscar la pertenencia del usuario al proyecto y comparar
        su rol con el rol solicitado. Devuelve True si coincide, False
        en caso contrario. Lanza EntidadNoEncontrada si el proyecto
        no existe.
        """
        raise NotImplementedError(
            "verificar_permiso no implementado — pendiente de asignación."
        )

    def listar_miembros(self, id_proyecto: str) -> list[MiembroProyecto]:
        """
        Devuelve todos los miembros de un proyecto.

        TODO: Implementar — asignado a otro integrante del equipo.
        Debe verificar que el proyecto exista (lanza EntidadNoEncontrada
        si no), luego buscar todos los registros en 'miembros' con
        id_proyecto coincidente y devolver una lista de MiembroProyecto.
        """
        raise NotImplementedError(
            "listar_miembros no implementado — pendiente de asignación."
        )
