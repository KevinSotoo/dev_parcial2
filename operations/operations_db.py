from sqlmodel import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from data.models import Usuario, EstadoUsuario, Tarea, EstadoTarea
from datetime import datetime

async def crear_usuario(usuario: Usuario, session: AsyncSession):
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)
    return usuario

async def obtener_usuarios(session: AsyncSession):
    result = await session.execute(select(Usuario))
    return result.scalars().all()

async def obtener_usuario(usuario_id: int, session: AsyncSession):
    usuario = await session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

async def actualizar_estado(usuario_id: int, nuevo_estado: EstadoUsuario, session: AsyncSession):
    usuario = await session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.estado = nuevo_estado
    await session.commit()
    await session.refresh(usuario)
    return usuario

async def actualizar_premium(usuario_id: int, premium: bool, session: AsyncSession):
    usuario = await session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.premium = premium
    await session.commit()
    await session.refresh(usuario)
    return usuario

async def usuarios_por_estado(estado: EstadoUsuario, session: AsyncSession):
    result = await session.execute(select(Usuario).where(Usuario.estado == estado))
    return result.scalars().all()

async def usuarios_premium_activos(session: AsyncSession):
    result = await session.execute(
        select(Usuario).where(Usuario.premium == True, Usuario.estado == EstadoUsuario.ACTIVO)
    )
    return result.scalars().all()

async def crear_tarea(tarea: Tarea, session: AsyncSession):
    if not tarea.nombre or not tarea.descripcion:
        raise HTTPException(status_code=400, detail="Nombre y descripción son obligatorios")

    if tarea.usuario_id is not None:
        usuario = await session.get(Usuario, tarea.usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario asignado no encontrado")

    tarea.fecha_creacion = datetime.now()
    tarea.fecha_modificacion = datetime.now()

    session.add(tarea)
    await session.commit()
    await session.refresh(tarea)
    return tarea

async def obtener_tareas(session: AsyncSession):
    result = await session.execute(select(Tarea))
    return result.scalars().all()

async def obtener_tarea(tarea_id: int, session: AsyncSession):
    tarea = await session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

async def actualizar_estado_tarea(tarea_id: int, nuevo_estado: EstadoTarea, session: AsyncSession):
    tarea = await session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tarea.estado = nuevo_estado
    tarea.fecha_modificacion = datetime.now()
    await session.commit()
    await session.refresh(tarea)
    return tarea

async def eliminar_tarea(tarea_id: int, session: AsyncSession):
    tarea = await session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    await session.delete(tarea)
    await session.commit()
    return {"detail": "Tarea eliminada correctamente"}
