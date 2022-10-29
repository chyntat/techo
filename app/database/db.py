from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.common.constants import *
engine = create_async_engine(database_url, echo=True, future=True, pool_size=25, max_overflow=25)

Base = declarative_base()
metadata = Base.metadata


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
