import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Optional
from sqlmodel import SQLModel, Session, select

load_dotenv()

CLEVER_USER = os.getenv('CLEVER_USER')
CLEVER_PASSWORD = os.getenv('CLEVER_PASSWORD')
CLEVER_HOST = os.getenv('CLEVER_HOST')
CLEVER_PORT = os.getenv('CLEVER_PORT')
CLEVER_DATABASE = os.getenv('CLEVER_DATABASE')

if not all([CLEVER_USER, CLEVER_PASSWORD, CLEVER_HOST, CLEVER_DATABASE]):
    raise ValueError("Faltan variables de entorno para la conexión a la base de datos")

port: Optional[int] = None
if CLEVER_PORT is not None:
    try:
        port = int(CLEVER_PORT)
    except ValueError:
        raise ValueError(f"Valor inválido para CLEVER_PORT: {CLEVER_PORT}")
else:
    port = 5432

CLEVER_DB = (
    f"postgresql+asyncpg://{CLEVER_USER}:"
    f"{CLEVER_PASSWORD}@"
    f"{CLEVER_HOST}:"
    f"{port}/"
    f"{CLEVER_DATABASE}"
)

engine: AsyncEngine = create_async_engine(CLEVER_DB, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
