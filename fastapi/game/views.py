from datetime import datetime
from fastapi import Depends, APIRouter
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select
from auth.provider import authorization
from db_config import engine
from game.models import Game, Stadium
from game.schemas import GameResponse

router = APIRouter()

@router.get('/games', response_model=list[GameResponse])
async def get_games(
    start_date: datetime, 
    end_date: datetime, 
    _: bool = Depends(authorization)
):
    with Session(engine) as session:
        # Query to filter games within the date range and include relationships
        games = (
            session.exec(
                select(Game)
                .where(Game.date >= start_date, Game.date <= end_date)
                .options(joinedload(Game.stadium), joinedload(Game.home_team), joinedload(Game.away_team))
            )
            .all()
        )
        
        # Format the response
        response = []
        for game in games:
            # Determine if the home team won or lost
            score = "W" if game.home_team_score > game.away_team_score else "L"
            ht = f"{game.home_team_score}-{game.away_team_score}"
            
            response.append(GameResponse(
                date=game.date.strftime("%B %d, %Y"),
                stadium=game.stadium.name,
                logo_uri=game.away_team.logo_uri,
                location=game.stadium.location,
                opponent=game.away_team.name,
                score=score,
                ht=ht
            ))
        
        return response
    
@router.post('/games')
async def create_team(game: Game, _: bool = Depends(authorization)):
    with Session(engine) as session:
        session.add(game)
        session.commit()
        session.refresh(game)
        return game

@router.get('/stadiums', response_model=list[Stadium])
async def get_stadiums(_: bool = Depends(authorization)):
    with Session(engine) as session:
        stadiums = session.exec(select(Game)).all()
        return stadiums
    
@router.post('/stadiums')
async def create_stadium(stadium: Stadium, _: bool = Depends(authorization)):
    with Session(engine) as session:
        session.add(stadium)
        session.commit()
        session.refresh(stadium)
        return stadium
