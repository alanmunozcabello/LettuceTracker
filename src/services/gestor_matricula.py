"""GestorMatricula — Lógica de negocio para la gestión de matrículas."""

from __future__ import annotations

import uuid

from src.models.matricula import Matricula
from src.services.excepciones import EntidadDuplicada, EntidadNoEncontrada, ReglaNegocioError
from src.services.persistencia_json import agregar_registro, buscar_registro, buscar_registros


class GestorMatricula:
    """Gestiona la inscripción de usuarios en cursos."""

    def validar_inscripcion(self, id_usuario: str, id_curso: str) -> None:
        """Verifica existencia de usuario y curso, y que no haya matrícula duplicada."""
        usuario = buscar_registro("usuarios", "id", id_usuario)
        if usuario is None:
            raise EntidadNoEncontrada("Usuario", id_usuario)

        curso = buscar_registro("cursos", "id", id_curso)
        if curso is None:
            raise EntidadNoEncontrada("Curso", id_curso)

        duplicados = buscar_registros("matriculas", filtros={"id_usuario": id_usuario, "id_curso": id_curso})
        if duplicados:
            raise EntidadDuplicada("Matrícula", f"usuario={id_usuario}, curso={id_curso}")

    def registrar_matricula(self, id_usuario: str, id_curso: str) -> Matricula:
        """Registra la matrícula tras validar las condiciones necesarias."""
        self.validar_inscripcion(id_usuario, id_curso)

        id_matricula = f"MAT-{uuid.uuid4().hex[:8].upper()}"
        matricula = Matricula(id_matricula=id_matricula, id_usuario=id_usuario, id_curso=id_curso)
        agregar_registro("matriculas", matricula.to_dict())
        return matricula

    # Métodos pendientes de implementación

    def buscar_matricula(self, id_matricula: str) -> Matricula:
        """TODO: buscar en 'matriculas' por 'id_matricula', lanzar EntidadNoEncontrada si no existe."""
        raise NotImplementedError("buscar_matricula no implementado.")

    def listar_matriculas(self, id_usuario: str | None = None, id_curso: str | None = None) -> list[Matricula]:
        """TODO: construir filtros y usar buscar_registros(), devolver lista de Matricula."""
        raise NotImplementedError("listar_matriculas no implementado.")
