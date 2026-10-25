"""
GestorMatricula — Lógica de negocio para la gestión de matrículas.

Métodos implementados (2 de 4):
  ✅ registrar_matricula
  ✅ validar_inscripcion

Métodos pendientes de implementación:
  ❌ buscar_matricula
  ❌ listar_matriculas

NOTA — Dependencias no verificables:
El repositorio no posee módulos de Usuarios ni Cursos. Las validaciones
de existencia se realizan contra los archivos JSON semilla provisionales
(src/data/usuarios.json y src/data/cursos.json).
"""

from __future__ import annotations

import uuid

from src.models.matricula import Matricula
from src.services.excepciones import EntidadDuplicada, EntidadNoEncontrada, ReglaNegocioError
from src.services.persistencia_json import (
    agregar_registro,
    buscar_registro,
    buscar_registros,
    cargar_coleccion,
)


class GestorMatricula:
    """Gestiona la inscripción de usuarios en cursos."""

    # ------------------------------------------------------------------ #
    # Métodos IMPLEMENTADOS
    # ------------------------------------------------------------------ #

    def validar_inscripcion(self, id_usuario: str, id_curso: str) -> None:
        """
        Verifica que el usuario y el curso existan y que no haya una
        matrícula duplicada para la misma combinación.

        Raises:
            EntidadNoEncontrada: si el usuario o el curso no existen.
            EntidadDuplicada: si la matrícula ya existe.
        """
        # Verificar existencia del usuario
        usuario = buscar_registro("usuarios", "id", id_usuario)
        if usuario is None:
            raise EntidadNoEncontrada("Usuario", id_usuario)

        # Verificar existencia del curso
        curso = buscar_registro("cursos", "id", id_curso)
        if curso is None:
            raise EntidadNoEncontrada("Curso", id_curso)

        # Verificar duplicados
        duplicados = buscar_registros(
            "matriculas",
            filtros={"id_usuario": id_usuario, "id_curso": id_curso},
        )
        if duplicados:
            raise EntidadDuplicada(
                "Matrícula",
                f"usuario={id_usuario}, curso={id_curso}",
            )

    def registrar_matricula(self, id_usuario: str, id_curso: str) -> Matricula:
        """
        Registra la matrícula de un usuario en un curso tras validar
        las condiciones necesarias.

        Raises:
            EntidadNoEncontrada: si el usuario o el curso no existen.
            EntidadDuplicada: si la matrícula ya existe.
        """
        self.validar_inscripcion(id_usuario, id_curso)

        id_matricula = f"MAT-{uuid.uuid4().hex[:8].upper()}"
        matricula = Matricula(
            id_matricula=id_matricula,
            id_usuario=id_usuario,
            id_curso=id_curso,
        )
        agregar_registro("matriculas", matricula.to_dict())
        return matricula

    # ------------------------------------------------------------------ #
    # Métodos PENDIENTES de implementación
    # ------------------------------------------------------------------ #

    def buscar_matricula(self, id_matricula: str) -> Matricula:
        """
        Busca una matrícula por su identificador.

        TODO: Implementar — asignado a otro integrante del equipo.
        Debe buscar en la colección 'matriculas' por 'id_matricula' y
        reconstruir la entidad con Matricula.from_dict(). Lanza
        EntidadNoEncontrada si no existe.
        """
        raise NotImplementedError(
            "buscar_matricula no implementado — pendiente de asignación."
        )

    def listar_matriculas(
        self, id_usuario: str | None = None, id_curso: str | None = None
    ) -> list[Matricula]:
        """
        Devuelve matrículas registradas, con filtros opcionales.

        TODO: Implementar — asignado a otro integrante del equipo.
        Debe construir un dict de filtros a partir de los parámetros
        no nulos y usar buscar_registros() para obtener los resultados.
        Devuelve una lista de entidades Matricula.
        """
        raise NotImplementedError(
            "listar_matriculas no implementado — pendiente de asignación."
        )
