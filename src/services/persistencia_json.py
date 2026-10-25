"""
Capa de persistencia JSON provisional.

ADVERTENCIA: Esta capa almacena los datos en archivos .json dentro de
src/data/. Los datos sobreviven reinicios del servidor pero NO proporcionan
garantías transaccionales, bloqueos ni protección contra escrituras
concurrentes. Es una solución provisional hasta que se integre una base de
datos real.

Archivos generados:
  - src/data/proyectos.json
  - src/data/matriculas.json
  - src/data/miembros.json
  - src/data/usuarios.json   (datos semilla provisionales)
  - src/data/cursos.json      (datos semilla provisionales)
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


# Directorio donde se almacenan los archivos JSON
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _asegurar_directorio() -> None:
    """Crea el directorio de datos si no existe."""
    _DATA_DIR.mkdir(parents=True, exist_ok=True)


def _ruta_archivo(nombre: str) -> Path:
    """Devuelve la ruta absoluta a un archivo JSON de datos."""
    return _DATA_DIR / f"{nombre}.json"


def cargar_coleccion(nombre: str) -> list[dict[str, Any]]:
    """
    Carga una colección completa desde un archivo JSON.

    Devuelve una lista vacía si el archivo no existe.
    """
    _asegurar_directorio()
    ruta = _ruta_archivo(nombre)
    if not ruta.exists():
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_coleccion(nombre: str, datos: list[dict[str, Any]]) -> None:
    """
    Guarda una colección completa en un archivo JSON.

    Sobrescribe el contenido anterior.
    """
    _asegurar_directorio()
    ruta = _ruta_archivo(nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def agregar_registro(nombre: str, registro: dict[str, Any]) -> None:
    """Agrega un registro al final de una colección JSON."""
    datos = cargar_coleccion(nombre)
    datos.append(registro)
    guardar_coleccion(nombre, datos)


def actualizar_registro(
    nombre: str,
    campo_clave: str,
    valor_clave: str,
    datos_actualizados: dict[str, Any],
) -> bool:
    """
    Actualiza un registro existente identificado por campo_clave == valor_clave.

    Devuelve True si encontró y actualizó el registro, False en caso contrario.
    """
    datos = cargar_coleccion(nombre)
    for i, reg in enumerate(datos):
        if reg.get(campo_clave) == valor_clave:
            datos[i].update(datos_actualizados)
            guardar_coleccion(nombre, datos)
            return True
    return False


def buscar_registro(
    nombre: str, campo: str, valor: str
) -> dict[str, Any] | None:
    """
    Busca el primer registro donde campo == valor.

    Devuelve None si no lo encuentra.
    """
    for reg in cargar_coleccion(nombre):
        if reg.get(campo) == valor:
            return reg
    return None


def buscar_registros(
    nombre: str, filtros: dict[str, str] | None = None
) -> list[dict[str, Any]]:
    """
    Devuelve todos los registros que coinciden con los filtros dados.

    Si filtros es None o vacío, devuelve todos los registros.
    """
    datos = cargar_coleccion(nombre)
    if not filtros:
        return datos
    return [
        reg
        for reg in datos
        if all(reg.get(k) == v for k, v in filtros.items())
    ]


# ============================================================
# Datos semilla provisionales
# ============================================================

def inicializar_datos_semilla() -> None:
    """
    Crea archivos de datos semilla si no existen.

    NOTA: El repositorio no posee módulos de Usuarios ni de Cursos.
    Se crean datos mínimos para poder validar la existencia de usuarios
    y cursos durante las operaciones de matrícula y asignación de miembros.
    Estos datos son PROVISIONALES.
    """
    _asegurar_directorio()

    # Usuarios semilla
    if not _ruta_archivo("usuarios").exists():
        usuarios = [
            {"id": "USR001", "nombre": "Nicolas Urbina", "email": "nurbina@alumnos.utalca.cl"},
            {"id": "USR002", "nombre": "Cristian Aliaga", "email": "caliaga@alumnos.utalca.cl"},
            {"id": "USR003", "nombre": "Alan Muñoz", "email": "amunoz@alumnos.utalca.cl"},
        ]
        guardar_coleccion("usuarios", usuarios)

    # Cursos semilla
    if not _ruta_archivo("cursos").exists():
        cursos = [
            {"id": "CUR001", "nombre": "Diseño de Software", "semestre": "2026-2"},
            {"id": "CUR002", "nombre": "Ingeniería de Software", "semestre": "2026-2"},
        ]
        guardar_coleccion("cursos", cursos)

    # Colecciones vacías
    for col in ("proyectos", "matriculas", "miembros"):
        if not _ruta_archivo(col).exists():
            guardar_coleccion(col, [])
