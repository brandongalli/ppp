from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

from player.models import Team

class Stadium(SQLModel, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    name: str = Field(unique=True, index=True)
    location: str
    
    games: list["Game"] = Relationship(back_populates="stadium")

class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    date: datetime = Field(default=None, nullable=False)
    home_team_score: int
    away_team_score: int

    stadium_id: int | None = Field(default=None, foreign_key='stadium.id')
    home_team_id: int | None = Field(default=None, foreign_key='team.id')
    away_team_id: int | None = Field(default=None, foreign_key='team.id')

    stadium: Optional[Stadium] = Relationship(
        back_populates="games",
        sa_relationship_kwargs={"foreign_keys": "Game.stadium_id"}
    )
    home_team: Optional[Team] = Relationship(
        back_populates="home_games", 
        sa_relationship_kwargs={"foreign_keys": "Game.home_team_id"}
    )
    away_team: Optional[Team] = Relationship(
        back_populates="away_games", 
        sa_relationship_kwargs={"foreign_keys": "Game.away_team_id"}
    )


    