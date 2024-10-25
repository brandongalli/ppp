from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, inspect, Relationship

class PositionChoices(str, Enum):
    Quarterback = 'QB'
    Center = 'C'
    RunningBack = 'RB'
    FullBack = 'FB'
    WideReceiver = 'WR'
    TightEnd = 'TE'
    LeftGuard = 'LG'
    LeftTackle = 'LT'
    Safety = 'S'
    DefensiveTackle = 'DT'
    DefensiveEnd = 'DE'
    LineBacker = 'LB'
    CornerBack = 'CB'
    Kicker = 'K'
    Putner = 'P'

class RankingChoices(str, Enum):
    WorldRanking = 'W'
    GameRanking = 'G'

class PlayerBase(SQLModel):
    first_name: str
    last_name: str
    team_id: int
    position: PositionChoices
    number: int
    height: float
    weight: float
    birth_year: int
    debut_year: int
    college: str
    bio: str

    def to_dict(self) -> dict:
        """
        Convert the SQLModel instance into a dictionary.
        """
        return self.model_dump(exclude_unset=True)

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    name: str = Field(default=None, nullable=False, unique=True, index=True)
    logo_uri: str # 49ers.png

    home_games: list["Game"] = Relationship(
        back_populates="home_team", 
        sa_relationship_kwargs={"foreign_keys": "Game.home_team_id"}
    )
    away_games: list["Game"] = Relationship(
        back_populates="away_team", 
        sa_relationship_kwargs={"foreign_keys": "Game.away_team_id"}
    )



class Player(PlayerBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    team_id: int = Field(foreign_key='team.id')


    def __init__(self, **kw):
        mapper = inspect(self).mapper
        for key in mapper.relationships:
            if key in kw:
                kw[key] = mapper.relationships[key].entity.class_(**kw[key])
        super().__init__(**kw)
    
class Rank(SQLModel, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    player_id: int = Field(foreign_key='player.id')
    ranking_type: RankingChoices
    game_id: int = Field(foreign_key='game.id')