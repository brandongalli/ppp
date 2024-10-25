import os
import json
import logging
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import sessionmaker

from game.models import Stadium, Game
from player.models import Player, Rank, Team

logging.basicConfig(level=logging.INFO)

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

def init_db():
    with engine.begin() as conn:
        # Optional: Drop tables if needed
        # conn.run_sync(SQLModel.metadata.drop_all)

        # Create all tables
        logging.info("Creating tables...")
        SQLModel.metadata.create_all(conn)
        logging.info("Tables created successfully.")
