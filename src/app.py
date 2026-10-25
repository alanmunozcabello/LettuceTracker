"""Punto de entrada de la aplicación FastAPI."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.route.administracion_routes import router as administracion_router
from src.route.autenticacion_routes import router as autenticacion_router
from src.services.persistencia_json import inicializar_datos_semilla

app = FastAPI(
    title="LettuceTracker API",
    description=(
        "API del sistema LettuceTracker — Gestión Documental de Proyectos. "
        "Universidad de Talca, Departamento de Ciencias de la Computación."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(administracion_router)
app.include_router(autenticacion_router)

@app.get("/")
def root():
    """Endpoint raíz."""
    return {"message": "Bienvenido a LettuceTracker API"}

@app.on_event("startup")
def startup_event():
    """Inicializa los datos semilla."""
    inicializar_datos_semilla()

@app.get("/health", tags=["Sistema"])
def health_check():
    """Endpoint de salud."""
    return {"status": "ok", "servicio": "LettuceTracker API", "version": "0.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)
