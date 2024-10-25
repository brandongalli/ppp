import os
import json
import logging
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from game.models import Stadium, Game
from player.models import Player, Rank, Team

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load database configuration from environment variables
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE = os.getenv("DATABASE")
DATABASE_PORT = int(os.getenv("DATABASE_PORT"))

# Create a synchronous engine for SQLModel ORM
engine = create_engine(
    f"mysql+mysqlconnector://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE}",
    echo=True,
    future=True
)

def init_db():
    """
    Initializes the database by creating all necessary tables.

    This function will:
    - Establish a connection to the database.
    - Create all tables defined in SQLModel metadata (if they do not already exist).
    - Log the creation process.

    Optional:
    - Uncomment `SQLModel.metadata.drop_all(conn)` to drop all tables before creation if resetting is needed.
    """
    with engine.begin() as conn:
        # Uncomment the next line to drop all tables (useful for resetting the database)
        # SQLModel.metadata.drop_all(conn)
        
        logging.info("Creating tables...")
        # Create tables from SQLModel metadata
        SQLModel.metadata.create_all(conn)
        logging.info("Tables created successfully.")
