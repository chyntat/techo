from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_async_engine("sqlite+aiosqlite:///./test.db")

Base = declarative_base()
metadata = Base.metadata


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with sessionmaker(engine, expire_on_commit=False, class_=AsyncSession) as session:
        try:
            yield session
        finally:
            await session.close()
