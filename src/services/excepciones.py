"""
Excepciones de dominio del módulo MD0008.

Estas excepciones representan errores de reglas de negocio y se transforman
en códigos HTTP apropiados en la capa de rutas.
"""


class EntidadNoEncontrada(Exception):
    """El recurso solicitado no existe. → 404"""

    def __init__(self, entidad: str, identificador: str) -> None:
        self.entidad = entidad
        self.identificador = identificador
        super().__init__(f"{entidad} con identificador '{identificador}' no encontrado.")


class EntidadDuplicada(Exception):
    """Se intentó crear un recurso que ya existe. → 409"""

    def __init__(self, entidad: str, identificador: str) -> None:
        self.entidad = entidad
        self.identificador = identificador
        super().__init__(f"{entidad} con identificador '{identificador}' ya existe.")


class ReglaNegocioError(Exception):
    """Violación de una regla de negocio. → 400"""

    def __init__(self, mensaje: str) -> None:
        self.mensaje = mensaje
        super().__init__(mensaje)
