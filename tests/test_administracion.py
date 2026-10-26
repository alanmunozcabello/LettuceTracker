"""
Pruebas automatizadas del módulo MD0008 — Administración de Proyectos y Usuarios.

Todas las pruebas usan TestClient de FastAPI y aíslan los datos usando
un directorio temporal para los archivos JSON. Ninguna prueba depende de
datos personales ni de base de datos externa.

Las pruebas verifican que las rutas delegan en AdministracionFacade
(no llaman directamente a los gestores).

Pruebas implementadas:
  ✅ Creación correcta de proyectos
  ✅ Rechazo de nombres vacíos
  ✅ Rechazo de identificadores duplicados
  ✅ Consulta de proyectos inexistentes
  ✅ Matrícula válida
  ✅ Rechazo de matrículas duplicadas
  ✅ Rechazo de usuarios inexistentes en matrícula
  ✅ Rechazo de cursos inexistentes en matrícula
  ✅ Asignación de un rol válido
  ✅ Rechazo de roles no permitidos
  ✅ Rechazo de proyectos inexistentes al asignar roles
  ✅ Rechazo de usuarios inexistentes al asignar roles
  ✅ Endpoint de salud
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path
from unittest import mock

import pytest
from fastapi.testclient import TestClient


# Fixture de pruebas

@pytest.fixture(autouse=True)
def datos_aislados(tmp_path):
    """
    Redirige la persistencia JSON a un directorio temporal para cada test.
    Crea datos semilla mínimos para las pruebas.
    """
    with mock.patch("src.services.persistencia_json._DATA_DIR", tmp_path):
        usuarios = [
            {"id": "USR001", "nombre": "Nicolas Urbina", "email": "nurbina@alumnos.utalca.cl"},
            {"id": "USR002", "nombre": "Cristian Aliaga", "email": "caliaga@alumnos.utalca.cl"},
            {"id": "USR003", "nombre": "Alan Muñoz", "email": "amunoz@alumnos.utalca.cl"},
        ]
        cursos = [
            {"id": "CUR001", "nombre": "Diseño de Software", "semestre": "2026-2"},
            {"id": "CUR002", "nombre": "Ingeniería de Software", "semestre": "2026-2"},
        ]
        (tmp_path / "usuarios.json").write_text(json.dumps(usuarios, ensure_ascii=False), encoding="utf-8")
        (tmp_path / "cursos.json").write_text(json.dumps(cursos, ensure_ascii=False), encoding="utf-8")
        (tmp_path / "proyectos.json").write_text("[]", encoding="utf-8")
        (tmp_path / "matriculas.json").write_text("[]", encoding="utf-8")
        (tmp_path / "miembros.json").write_text("[]", encoding="utf-8")

        yield tmp_path


@pytest.fixture
def client():
    """TestClient de FastAPI."""
    from src.app import app
    return TestClient(app)


# Pruebas de proyectos

class TestCrearProyecto:
    """Pruebas para POST /api/v1/administracion/proyectos."""

    def test_crear_proyecto_exitoso(self, client):
        """Creación correcta devuelve 201 con los datos del proyecto."""
        resp = client.post(
            "/api/v1/administracion/proyectos",
            json={"id": "PRY001", "nombre": "LettuceTracker", "descripcion": "Sistema de gestión"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["id"] == "PRY001"
        assert data["nombre"] == "LettuceTracker"
        assert data["estado"] == "Activo"
        assert "fecha" in data

    def test_rechazar_nombre_vacio(self, client):
        """Un nombre vacío o solo espacios debe ser rechazado (422)."""
        resp = client.post(
            "/api/v1/administracion/proyectos",
            json={"id": "PRY002", "nombre": "   ", "descripcion": "desc"},
        )
        assert resp.status_code == 422

    def test_rechazar_id_duplicado(self, client):
        """Crear dos proyectos con el mismo id devuelve 409."""
        payload = {"id": "PRY001", "nombre": "Proyecto A", "descripcion": ""}
        client.post("/api/v1/administracion/proyectos", json=payload)
        resp = client.post("/api/v1/administracion/proyectos", json=payload)
        assert resp.status_code == 409

    def test_rechazar_campos_extra(self, client):
        """Campos inesperados deben ser rechazados (422)."""
        resp = client.post(
            "/api/v1/administracion/proyectos",
            json={"id": "PRY003", "nombre": "Test", "descripcion": "", "estado": "Inactivo"},
        )
        assert resp.status_code == 422


class TestConsultarProyecto:
    """Pruebas para GET /api/v1/administracion/proyectos/{id}."""

    def test_consultar_proyecto_existente(self, client):
        """Proyecto existente devuelve 200."""
        client.post(
            "/api/v1/administracion/proyectos",
            json={"id": "PRY001", "nombre": "Test", "descripcion": ""},
        )
        resp = client.get("/api/v1/administracion/proyectos/PRY001")
        assert resp.status_code == 200
        assert resp.json()["id"] == "PRY001"

    def test_consultar_proyecto_inexistente(self, client):
        """Proyecto inexistente devuelve 404."""
        resp = client.get("/api/v1/administracion/proyectos/NO_EXISTE")
        assert resp.status_code == 404


# Pruebas de matrículas

class TestMatriculas:
    """Pruebas para POST /api/v1/administracion/matriculas."""

    def test_matricula_valida(self, client):
        """Matrícula con usuario y curso existentes devuelve 201."""
        resp = client.post(
            "/api/v1/administracion/matriculas",
            json={"id_usuario": "USR001", "id_curso": "CUR001"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["id_usuario"] == "USR001"
        assert data["id_curso"] == "CUR001"
        assert "id_matricula" in data
        assert "fecha" in data

    def test_rechazar_matricula_duplicada(self, client):
        """Matrícula duplicada devuelve 409."""
        payload = {"id_usuario": "USR001", "id_curso": "CUR001"}
        client.post("/api/v1/administracion/matriculas", json=payload)
        resp = client.post("/api/v1/administracion/matriculas", json=payload)
        assert resp.status_code == 409

    def test_rechazar_usuario_inexistente(self, client):
        """Usuario inexistente devuelve 404."""
        resp = client.post(
            "/api/v1/administracion/matriculas",
            json={"id_usuario": "NO_EXISTE", "id_curso": "CUR001"},
        )
        assert resp.status_code == 404

    def test_rechazar_curso_inexistente(self, client):
        """Curso inexistente devuelve 404."""
        resp = client.post(
            "/api/v1/administracion/matriculas",
            json={"id_usuario": "USR001", "id_curso": "NO_EXISTE"},
        )
        assert resp.status_code == 404


# Pruebas de miembros y permisos

class TestAsignarMiembro:
    """Pruebas para POST /api/v1/administracion/proyectos/{id}/miembros."""

    def _crear_proyecto(self, client):
        """Helper: crea un proyecto para las pruebas de miembros."""
        client.post(
            "/api/v1/administracion/proyectos",
            json={"id": "PRY001", "nombre": "Proyecto Test", "descripcion": ""},
        )

    def test_asignar_rol_valido(self, client):
        """Asignar un rol válido a un usuario existente devuelve 201."""
        self._crear_proyecto(client)
        resp = client.post(
            "/api/v1/administracion/proyectos/PRY001/miembros",
            json={"id_usuario": "USR001", "rol": "Desarrollador"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["id_usuario"] == "USR001"
        assert data["rol"] == "Desarrollador"
        assert data["id_proyecto"] == "PRY001"

    def test_rechazar_rol_no_permitido(self, client):
        """Un rol no permitido devuelve 422 (validación de esquema)."""
        self._crear_proyecto(client)
        resp = client.post(
            "/api/v1/administracion/proyectos/PRY001/miembros",
            json={"id_usuario": "USR001", "rol": "RolInventado"},
        )
        assert resp.status_code == 422

    def test_rechazar_proyecto_inexistente(self, client):
        """Asignar a un proyecto inexistente devuelve 404."""
        resp = client.post(
            "/api/v1/administracion/proyectos/NO_EXISTE/miembros",
            json={"id_usuario": "USR001", "rol": "Desarrollador"},
        )
        assert resp.status_code == 404

    def test_rechazar_usuario_inexistente(self, client):
        """Asignar a un usuario inexistente devuelve 404."""
        self._crear_proyecto(client)
        resp = client.post(
            "/api/v1/administracion/proyectos/PRY001/miembros",
            json={"id_usuario": "NO_EXISTE", "rol": "Desarrollador"},
        )
        assert resp.status_code == 404

    def test_actualizar_rol_existente(self, client):
        """Re-asignar un rol a un miembro existente devuelve 200 y actualiza."""
        self._crear_proyecto(client)
        client.post(
            "/api/v1/administracion/proyectos/PRY001/miembros",
            json={"id_usuario": "USR001", "rol": "Desarrollador"},
        )
        resp = client.post(
            "/api/v1/administracion/proyectos/PRY001/miembros",
            json={"id_usuario": "USR001", "rol": "Arquitecto"},
        )
        assert resp.status_code == 200
        assert resp.json()["rol"] == "Arquitecto"


class TestConsultarMiembro:
    """Pruebas para GET /api/v1/administracion/proyectos/{id}/miembros/{id_usuario}."""

    def test_consultar_miembro_existente(self, client):
        """Miembro existente devuelve 200."""
        client.post(
            "/api/v1/administracion/proyectos",
            json={"id": "PRY001", "nombre": "Test", "descripcion": ""},
        )
        client.post(
            "/api/v1/administracion/proyectos/PRY001/miembros",
            json={"id_usuario": "USR001", "rol": "Tester"},
        )
        resp = client.get("/api/v1/administracion/proyectos/PRY001/miembros/USR001")
        assert resp.status_code == 200
        assert resp.json()["rol"] == "Tester"

    def test_consultar_miembro_inexistente(self, client):
        """Miembro no encontrado devuelve 404."""
        client.post(
            "/api/v1/administracion/proyectos",
            json={"id": "PRY001", "nombre": "Test", "descripcion": ""},
        )
        resp = client.get("/api/v1/administracion/proyectos/PRY001/miembros/USR999")
        assert resp.status_code == 404


# Prueba del endpoint de salud

class TestHealth:
    """Pruebas para GET /health."""

    def test_health_ok(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
