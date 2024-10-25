from pydantic import BaseModel

class GameResponse(BaseModel):
    date: str
    stadium: str
    logo_uri: str
    location: str
    opponent: str
    score: str
    ht: str
    home_team_id: int
    away_team_id: int