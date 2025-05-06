from sqlmodel import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from data.models import Usuario, EstadoUsuario


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
