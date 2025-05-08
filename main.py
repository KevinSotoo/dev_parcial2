from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from data.models import Usuario, EstadoUsuario, Tarea, EstadoTarea
from utils.connection_db import init_db, get_session
from operations import operations_db as ops
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.post("/usuarios/", response_model=Usuario)
async def crear(usuario: Usuario, session: AsyncSession = Depends(get_session)):
    try:
        return await ops.crear_usuario(usuario, session)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error al crear el usuario en la base de datos")

@app.get("/usuarios/", response_model=List[Usuario])
async def listar(session: AsyncSession = Depends(get_session)):
    try:
        return await ops.obtener_usuarios(session)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error al obtener los usuarios")

@app.get("/usuarios/{usuario_id}", response_model=Usuario)
async def obtener(usuario_id: int, session: AsyncSession = Depends(get_session)):
    try:
        return await ops.obtener_usuario(usuario_id, session)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@app.get("/usuarios/estado/{estado}", response_model=List[Usuario])
async def filtrar_por_estado(estado: EstadoUsuario, session: AsyncSession = Depends(get_session)):
    try:
        return await ops.usuarios_por_estado(estado, session)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error al filtrar usuarios por estado")

@app.put("/usuarios/{usuario_id}/premium", response_model=Usuario)
async def hacer_premium(usuario_id: int, session: AsyncSession = Depends(get_session)):
    try:
        return await ops.marcar_como_premium(usuario_id, session)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@app.get("/usuarios/premium/activos", response_model=List[Usuario])
async def premium_y_activos(session: AsyncSession = Depends(get_session)):
    try:
        usuarios = await ops.usuarios_premium_activos(session)
        if not usuarios:
            raise HTTPException(status_code=404, detail="No hay usuarios premium y activos")
        return usuarios
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error al obtener usuarios premium y activos")

@app.post("/tareas/", response_model=Tarea)
async def crear_tarea(tarea: Tarea, session: AsyncSession = Depends(get_session)):
    try:
        return await ops.crear_tarea(tarea, session)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error al crear la tarea")

@app.get("/tareas/", response_model=List[Tarea])
async def listar_tareas(session: AsyncSession = Depends(get_session)):
    try:
        return await ops.obtener_tareas(session)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error al obtener las tareas")

@app.get("/tareas/{tarea_id}", response_model=Tarea)
async def obtener_tarea(tarea_id: int, session: AsyncSession = Depends(get_session)):
    try:
        return await ops.obtener_tarea(tarea_id, session)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@app.put("/tareas/{tarea_id}/estado", response_model=Tarea)
async def cambiar_estado_tarea(tarea_id: int, nuevo_estado: EstadoTarea, session: AsyncSession = Depends(get_session)):
    try:
        return await ops.actualizar_estado_tarea(tarea_id, nuevo_estado, session)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error al actualizar el estado de la tarea")

@app.delete("/tareas/{tarea_id}")
async def eliminar_tarea(tarea_id: int, session: AsyncSession = Depends(get_session)):
    try:
        return await ops.eliminar_tarea(tarea_id, session)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error al eliminar la tarea")
