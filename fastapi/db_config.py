import os

from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker, Session

from sqlalchemy.orm import sessionmaker


DATABASE_HOST= os.getenv("DATABASE_HOST")
DATABASE_USERNAME= os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD= os.getenv("DATABASE_PASSWORD")
DATABASE= os.getenv("DATABASE")
DATABASE_PORT= int(os.getenv("DATABASE_PORT"))
engine = create_engine(
    f"mysql+mysqlconnector://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@mysql_db:{DATABASE_PORT}/{DATABASE}",
    echo=True,
    future=True
)

# Synchronous version of init_db
def init_db():
    with engine.begin() as conn:
        # conn.run_sync(SQLModel.metadata.drop_all)
        SQLModel.metadata.create_all(conn)

def get_session() -> Session: # type: ignore
    sync_session = sessionmaker(
        engine, class_=Session, expire_on_commit=False
    )
    with sync_session() as session:
        yield session