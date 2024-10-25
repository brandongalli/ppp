from typing import Optional, List
from datetime import datetime
from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from auth.provider import authorization
from db_config import engine
from game.models import Game, Stadium
from game.schemas import GameResponse

router = APIRouter()

@router.get('/games', response_model=List[GameResponse])
async def get_games(
    start_date: Optional[datetime] = Query(None, description="Start date in yyyy-mm-dd format"),
    end_date: Optional[datetime] = Query(None, description="End date in yyyy-mm-dd format"),
    home_team_id: Optional[int] = Query(None, description="Home team ID"),
    _: bool = Depends(authorization)
):
    """
    Retrieve a list of games filtered by date and home team ID.

    Parameters:
    - start_date: Filter for games occurring on or after this date.
    - end_date: Filter for games occurring on or before this date.
    - home_team_id: Filter for games with the specified home team.

    Returns:
    - List of games with detailed information, formatted as GameResponse.
    """
    with Session(engine) as session:
        # Start building the base query with relationships for stadium and teams
        query = select(Game).options(
            joinedload(Game.stadium),
            joinedload(Game.home_team),
            joinedload(Game.away_team)
        )
        
        # Apply filters if parameters are provided
        if start_date:
            query = query.where(Game.date >= start_date)
        if end_date:
            query = query.where(Game.date <= end_date)
        if home_team_id:
            query = query.where(Game.home_team_id == home_team_id)

        # Execute the filtered query
        games = session.exec(query).all()
        
        # Format the response for each game
        response = []
        for game in games:
            # Determine if the home team won or lost
            score = "W" if game.home_team_score > game.away_team_score else "L"
            ht = f"{game.home_team_score}-{game.away_team_score}"
            
            response.append(GameResponse(
                date=game.date.strftime("%Y-%m-%d"),  # Format date as 'yyyy-mm-dd'
                stadium=game.stadium.name,
                logo_uri=game.away_team.logo_uri,
                location=game.stadium.location,
                opponent=game.away_team.name,
                score=score,
                ht=ht,
                home_team_id=game.home_team_id,
                away_team_id=game.away_team_id
            ))
        
        return response

@router.post('/games', response_model=Game)
async def create_game(game: Game, _: bool = Depends(authorization)):
    """
    Create a new game record.

    Parameters:
    - game: Game object with all necessary details.

    Returns:
    - The created game record.
    """
    with Session(engine) as session:
        session.add(game)
        session.commit()
        session.refresh(game)
        return game

@router.get('/stadiums', response_model=List[Stadium])
async def get_stadiums(_: bool = Depends(authorization)):
    """
    Retrieve a list of all stadiums.

    Returns:
    - List of all stadiums in the database.
    """
    with Session(engine) as session:
        # Query all stadiums from the database
        stadiums = session.exec(select(Stadium)).all()
        return stadiums

@router.post('/stadiums', response_model=Stadium)
async def create_stadium(stadium: Stadium, _: bool = Depends(authorization)):
    """
    Create a new stadium record.

    Parameters:
    - stadium: Stadium object with all necessary details.

    Returns:
    - The created stadium record.
    """
    with Session(engine) as session:
        session.add(stadium)
        session.commit()
        session.refresh(stadium)
        return stadium
