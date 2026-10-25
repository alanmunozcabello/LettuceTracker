"""Rutas HTTP del módulo MD0008 — Administración de Proyectos y Usuarios."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import JSONResponse

from src.models.schemas import (
    MiembroProyectoCreate,
    MiembroProyectoResponse,
    MatriculaCreate,
    MatriculaResponse,
    ProyectoCreate,
    ProyectoResponse,
    VerificarPermisoRequest,
    VerificarPermisoResponse,
)
from src.services.administracion_facade import AdministracionFacade
from src.services.excepciones import EntidadDuplicada, EntidadNoEncontrada, ReglaNegocioError

router = APIRouter(prefix="/api/v1/administracion", tags=["Administración"])
_facade = AdministracionFacade()


def _manejar_excepcion(e: Exception) -> None:
    """Transforma excepciones de dominio en HTTPException."""
    if isinstance(e, EntidadNoEncontrada):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    if isinstance(e, EntidadDuplicada):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    if isinstance(e, ReglaNegocioError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if isinstance(e, NotImplementedError):
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=str(e))
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor.")


# Proyectos

@router.post("/proyectos", response_model=ProyectoResponse, status_code=status.HTTP_201_CREATED, summary="Crear un proyecto")
def crear_proyecto(datos: ProyectoCreate):
    """Crea un nuevo proyecto con estado inicial 'Activo'."""
    try:
        proyecto = _facade.crear_proyecto(id=datos.id, nombre=datos.nombre, descripcion=datos.descripcion)
        return ProyectoResponse(**proyecto.to_dict())
    except (EntidadDuplicada, EntidadNoEncontrada, ReglaNegocioError, NotImplementedError) as e:
        _manejar_excepcion(e)


@router.get("/proyectos/{id_proyecto}", response_model=ProyectoResponse, summary="Consultar un proyecto")
def consultar_proyecto(id_proyecto: str):
    """Obtiene un proyecto específico por su identificador."""
    try:
        proyecto = _facade.consultar_proyecto(id_proyecto)
        return ProyectoResponse(**proyecto.to_dict())
    except (EntidadNoEncontrada, NotImplementedError) as e:
        _manejar_excepcion(e)


@router.get("/proyectos", response_model=list[ProyectoResponse], summary="Listar proyectos")
def listar_proyectos():
    """Lista todos los proyectos registrados. TODO: pendiente de implementación."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="listar_proyectos no implementado.")


# Matrículas

@router.post("/matriculas", response_model=MatriculaResponse, status_code=status.HTTP_201_CREATED, summary="Matricular un estudiante")
def matricular_estudiante(datos: MatriculaCreate):
    """Registra la matrícula de un usuario en un curso."""
    try:
        matricula = _facade.matricular_estudiante(id_usuario=datos.id_usuario, id_curso=datos.id_curso)
        return MatriculaResponse(**matricula.to_dict())
    except (EntidadDuplicada, EntidadNoEncontrada, ReglaNegocioError, NotImplementedError) as e:
        _manejar_excepcion(e)


@router.get("/matriculas/{id_matricula}", response_model=MatriculaResponse, summary="Consultar una matrícula")
def consultar_matricula(id_matricula: str):
    """Consulta una matrícula por su identificador. TODO: pendiente de implementación."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="consultar_matricula no implementado.")


@router.get("/matriculas", response_model=list[MatriculaResponse], summary="Listar matrículas")
def listar_matriculas(
    id_usuario: str | None = Query(default=None, description="Filtrar por usuario"),
    id_curso: str | None = Query(default=None, description="Filtrar por curso"),
):
    """Lista matrículas con filtros opcionales. TODO: pendiente de implementación."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="listar_matriculas no implementado.")


# Miembros y permisos

@router.post("/proyectos/{id_proyecto}/miembros", response_model=MiembroProyectoResponse, summary="Asignar miembro a un proyecto")
def asignar_miembro(id_proyecto: str, datos: MiembroProyectoCreate):
    """Asigna un usuario como miembro de un proyecto. Si ya es miembro, actualiza su rol."""
    try:
        miembro, es_nuevo = _facade.asignar_permiso(id_proyecto=id_proyecto, id_usuario=datos.id_usuario, rol=datos.rol)
        respuesta = MiembroProyectoResponse(**miembro.to_dict())
        if es_nuevo:
            return JSONResponse(content=respuesta.model_dump(), status_code=status.HTTP_201_CREATED)
        return respuesta
    except (EntidadDuplicada, EntidadNoEncontrada, ReglaNegocioError, NotImplementedError) as e:
        _manejar_excepcion(e)


@router.get("/proyectos/{id_proyecto}/miembros/{id_usuario}", response_model=MiembroProyectoResponse, summary="Consultar miembro de un proyecto")
def consultar_miembro(id_proyecto: str, id_usuario: str):
    """Consulta la pertenencia de un usuario a un proyecto."""
    try:
        miembro = _facade.consultar_miembro(id_proyecto, id_usuario)
        return MiembroProyectoResponse(**miembro.to_dict())
    except (EntidadNoEncontrada, NotImplementedError) as e:
        _manejar_excepcion(e)


@router.get("/proyectos/{id_proyecto}/miembros/{id_usuario}/permisos", response_model=MiembroProyectoResponse, summary="Consultar permisos de un miembro")
def consultar_permisos_miembro(id_proyecto: str, id_usuario: str):
    """Consulta el rol/permisos de un miembro en un proyecto."""
    try:
        miembro = _facade.consultar_miembro(id_proyecto, id_usuario)
        return MiembroProyectoResponse(**miembro.to_dict())
    except (EntidadNoEncontrada, NotImplementedError) as e:
        _manejar_excepcion(e)


@router.get("/proyectos/{id_proyecto}/miembros", response_model=list[MiembroProyectoResponse], summary="Listar miembros de un proyecto")
def listar_miembros(id_proyecto: str):
    """Lista los integrantes de un proyecto. TODO: pendiente de implementación."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="listar_miembros no implementado.")


@router.post("/proyectos/{id_proyecto}/miembros/{id_usuario}/verificar-permiso", response_model=VerificarPermisoResponse, summary="Verificar permiso de un miembro")
def verificar_permiso(id_proyecto: str, id_usuario: str, datos: VerificarPermisoRequest):
    """Verifica si un usuario tiene un rol específico en un proyecto. TODO: pendiente de implementación."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="verificar_permiso no implementado.")
