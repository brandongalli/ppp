from typing import Optional, List
from fastapi import Depends, APIRouter, Query
from sqlmodel import Session, select
from auth.provider import authorization
from db_config import engine
from player.models import Player, Team, Rank
from player.schemas import PlayerCreate, TeamCreate
from player.tasks import create_player_task, create_team_task

router = APIRouter()

@router.get('/teams', response_model=List[Team])
async def get_teams(_: bool = Depends(authorization)):
    """
    Retrieve a list of all teams.

    Returns:
    - List of Team objects.
    """
    with Session(engine) as session:
        teams = session.exec(select(Team)).all()
        return teams

@router.post('/teams')
async def create_team(team: TeamCreate, _: bool = Depends(authorization)):
    """
    Create a new team asynchronously.

    Parameters:
    - team: TeamCreate object containing team details.

    Returns:
    - The task result of the team creation.
    """
    # Initiate the async task for creating a team
    task = create_team_task(Team(**team.dict()))
    return task

@router.get('/players', response_model=List[Player])
async def get_players(
    _: bool = Depends(authorization),
    teams: Optional[str] = Query(None, description="Comma-separated team IDs to filter players by team")
):
    """
    Retrieve a list of players, optionally filtered by team IDs.

    Parameters:
    - teams: A comma-separated string of team IDs.

    Returns:
    - List of Player objects.
    """
    with Session(engine) as session:
        query = select(Player)
        
        # Apply team filter if provided
        if teams:
            team_ids = [int(team_id) for team_id in teams.split(',')]
            query = query.where(Player.team_id.in_(team_ids))
        
        players = session.exec(query).all()
        return players

@router.post('/players')
async def create_player(player: PlayerCreate, _: bool = Depends(authorization)):
    """
    Create a new player asynchronously.

    Parameters:
    - player: PlayerCreate object containing player details.

    Returns:
    - The task result of the player creation.
    """
    # Validate and initiate the async task for creating a player
    valid_player = Player.model_validate(player)
    task = create_player_task(valid_player)
    return task

@router.get('/rankings', response_model=List[Rank])
async def get_rankings(_: bool = Depends(authorization)):
    """
    Retrieve a list of all player rankings.

    Returns:
    - List of Rank objects.
    """
    with Session(engine) as session:
        ranking = session.exec(select(Rank)).all()
        return ranking

@router.post('/rankings')
async def create_ranking(ranking: Rank, _: bool = Depends(authorization)):
    """
    Create a new ranking entry.

    Parameters:
    - ranking: Rank object containing ranking details.

    Returns:
    - The created Rank object.
    """
    with Session(engine) as session:
        session.add(ranking)
        session.commit()
        session.refresh(ranking)
        return ranking
