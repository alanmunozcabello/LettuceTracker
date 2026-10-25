"""Pruebas del login provisional contra usuarios almacenados en JSON."""

from __future__ import annotations

import json
from unittest import mock

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path):
    """Cliente con una colección de usuarios aislada."""
    usuarios = [
        {
            "id": "USR001",
            "nombre": "Nicolas Urbina",
            "email": "nurbina@alumnos.utalca.cl",
            "contrasena": "nurbina123",
        }
    ]
    (tmp_path / "usuarios.json").write_text(json.dumps(usuarios), encoding="utf-8")

    with mock.patch("src.services.persistencia_json._DATA_DIR", tmp_path):
        from src.app import app

        yield TestClient(app)


def test_login_exitoso(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "NURBINA@ALUMNOS.UTALCA.CL", "contrasena": "nurbina123"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "autenticado": True,
        "usuario": {
            "id": "USR001",
            "nombre": "Nicolas Urbina",
            "email": "nurbina@alumnos.utalca.cl",
        },
    }


@pytest.mark.parametrize(
    "credenciales",
    [
        {"email": "nurbina@alumnos.utalca.cl", "contrasena": "incorrecta"},
        {"email": "otro@alumnos.utalca.cl", "contrasena": "nurbina123"},
    ],
)
def test_login_rechaza_credenciales_invalidas(client, credenciales):
    response = client.post("/api/v1/auth/login", json=credenciales)

    assert response.status_code == 401
    assert response.json()["detail"] == "Correo o contraseña incorrectos."


def test_login_rechaza_campos_extra(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "nurbina@alumnos.utalca.cl",
            "contrasena": "nurbina123",
            "rol": "admin",
        },
    )

    assert response.status_code == 422
