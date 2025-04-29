from sqlmodel import Field,SQLModel
from typing import Optional, List
from enum import Enum

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str=Field(nullable=False)
    email:str=Field(nullable=False)
    estado:Estadosuario=Field(default=EstadoUsuario.ACTIVO)
    premium:bool=Field(nullable=False)

class EstadoUsuario(str,Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"
    ELIminado = "ELIMINADO"
