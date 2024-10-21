import os

from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.orm import sessionmaker


DATABASE_HOST= os.getenv("DATABASE_HOST")
DATABASE_USERNAME= os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD= os.getenv("DATABASE_PASSWORD")
DATABASE= os.getenv("DATABASE")
DATABASE_PORT= int(os.getenv("DATABASE_PORT"))
engine = create_async_engine(
    f"mysql+mysqlconnector://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@mysql_db:{DATABASE_PORT}/{DATABASE}",
    echo=True,
    future=True
)

async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession: # type: ignore
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session