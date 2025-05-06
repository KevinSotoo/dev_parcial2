from sqlmodel import Field, SQLModel
from typing import Optional
from enum import Enum

class EstadoUsuario(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"
    ELIMINADO = "ELIMINADO"

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    estado: EstadoUsuario = Field(default=EstadoUsuario.ACTIVO)
    premium: bool
