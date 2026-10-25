"""
LettuceTracker — Punto de entrada de la aplicación FastAPI.

Módulo MD0008: Administración de Proyectos y Usuarios.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.route.administracion_routes import router as administracion_router
from src.services.persistencia_json import inicializar_datos_semilla

# ============================================================
# Crear la aplicación
# ============================================================

app = FastAPI(
    title="LettuceTracker API",
    description=(
        "API del sistema LettuceTracker — Gestión Documental de Proyectos. "
        "Universidad de Talca, Departamento de Ciencias de la Computación."
    ),
    version="0.1.0",
)

# ============================================================
# CORS — permite peticiones del frontend (ajustar en producción)
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restringir en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Archivos estáticos (frontend existente)
# ============================================================

app.mount("/static", StaticFiles(directory="src/static"), name="static")

# ============================================================
# Registrar routers
# ============================================================

app.include_router(administracion_router)

# ============================================================
# Inicialización de datos semilla
# ============================================================

@app.on_event("startup")
def startup_event():
    """Crea los archivos JSON semilla si no existen al iniciar."""
    inicializar_datos_semilla()

# ============================================================
# Endpoint de salud
# ============================================================

@app.get("/health", tags=["Sistema"])
def health_check():
    """Comprobación de salud del servicio."""
    return {"status": "ok", "servicio": "LettuceTracker API", "version": "0.1.0"}


# ============================================================
# Ejecución directa con Uvicorn
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)
