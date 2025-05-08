from sqlmodel import Field, SQLModel
from typing import Optional
from enum import Enum
from datetime import datetime



class EstadoUsuario(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"
    ELIMINADO = "ELIMINADO"


class EstadoTarea(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_PROGRESO = "EN_PROGRESO"
    COMPLETADA = "COMPLETADA"
    CANCELADA = "CANCELADA"


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    estado: EstadoUsuario = Field(default=EstadoUsuario.ACTIVO)
    premium: bool


class Tarea(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    descripcion: str = Field(nullable=False)
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    fecha_modificacion: datetime = Field(default_factory=datetime.now)
    estado: EstadoTarea = Field(default=EstadoTarea.PENDIENTE)
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")