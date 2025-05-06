from fastapi import FastAPI, Depends
from data.models import Usuario, EstadoUsuario
from utils.connection_db import init_db, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from operations import operations_db as ops
from typing import List

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.post("/usuarios/", response_model=Usuario)
async def crear(usuario: Usuario, session: AsyncSession = Depends(get_session)):
    return await ops.crear_usuario(usuario, session)


@app.get("/usuarios/", response_model=List[Usuario])
async def listar(session: AsyncSession = Depends(get_session)):
    return await ops.obtener_usuarios(session)


@app.get("/usuarios/{usuario_id}", response_model=Usuario)
async def obtener(usuario_id: int, session: AsyncSession = Depends(get_session)):
    return await ops.obtener_usuario(usuario_id, session)


@app.put("/usuarios/{usuario_id}/estado", response_model=Usuario)
async def actualizar_estado(usuario_id: int, nuevo_estado: EstadoUsuario, session: AsyncSession = Depends(get_session)):
    return await ops.actualizar_estado(usuario_id, nuevo_estado, session)


@app.put("/usuarios/{usuario_id}/premium", response_model=Usuario)
async def hacer_premium(usuario_id: int, session: AsyncSession = Depends(get_session)):
    return await ops.marcar_como_premium(usuario_id, session)


@app.get("/usuarios/estado/{estado}", response_model=List[Usuario])
async def filtrar_por_estado(estado: EstadoUsuario, session: AsyncSession = Depends(get_session)):
    return await ops.filtrar_por_estado(estado, session)


@app.get("/usuarios/premium/activos", response_model=List[Usuario])
async def premium_y_activos(session: AsyncSession = Depends(get_session)):
    return await ops.filtrar_premium_activos(session)
