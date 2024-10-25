from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from player.models import Team

class Stadium(SQLModel, table=True):
    """
    Represents a stadium where games are held.

    Attributes:
    - id: Primary key, uniquely identifies each stadium.
    - name: Unique name of the stadium.
    - location: Location of the stadium.
    - games: Relationship to the Game model, linking games played in this stadium.
    """
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    name: str = Field(unique=True, index=True)
    location: str
    
    games: List["Game"] = Relationship(back_populates="stadium")


class Game(SQLModel, table=True):
    """
    Represents a game played between teams at a stadium.

    Attributes:
    - id: Primary key, uniquely identifies each game.
    - date: Date and time the game is scheduled.
    - home_team_score: Score of the home team.
    - away_team_score: Score of the away team.
    - stadium_id: Foreign key linking to the Stadium where the game is held.
    - home_team_id: Foreign key linking to the home Team.
    - away_team_id: Foreign key linking to the away Team.
    - stadium: Relationship to the Stadium model.
    - home_team: Relationship to the Team model as the home team.
    - away_team: Relationship to the Team model as the away team.
    """
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    date: datetime = Field(default=None, nullable=False)
    home_team_score: int
    away_team_score: int

    stadium_id: Optional[int] = Field(default=None, foreign_key="stadium.id")
    home_team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    away_team_id: Optional[int] = Field(default=None, foreign_key="team.id")

    stadium: Optional[Stadium] = Relationship(
        back_populates="games",
        sa_relationship_kwargs={"foreign_keys": "Game.stadium_id"}
    )
    home_team: Optional["Team"] = Relationship(
        back_populates="home_games",
        sa_relationship_kwargs={"foreign_keys": "Game.home_team_id"}
    )
    away_team: Optional["Team"] = Relationship(
        back_populates="away_games",
        sa_relationship_kwargs={"foreign_keys": "Game.away_team_id"}
    )
