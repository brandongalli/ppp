from fastapi import Depends, APIRouter, HTTPException
from celery.result import AsyncResult
from sqlmodel import Session, select
from auth.provider import authorization
import asyncio
from db_config import engine
from player.models import Player, Team, Rank
from player.schemas import PlayerCreate, TeamCreate
from player.tasks import get_players_task, create_player_task, example_task, create_team_task
from worker.celery_worker import celery_app

router = APIRouter()

@router.get('/teams', response_model=list[Team])
async def get_teams(_: bool = Depends(authorization)):
    with Session(engine) as session:
        teams = session.exec(select(Team)).all()
        return teams
    
@router.post('/teams')
async def create_team(team: TeamCreate, _: bool = Depends(authorization)):
    task = create_team_task(Team(**team.dict()))

    return task

@router.get('/players', response_model=list[Player])
async def get_players(_: bool = Depends(authorization)):
    with Session(engine) as session:
        players = session.exec(select(Player)).all()
        return players
    
@router.post('/players')
async def create_player(player: PlayerCreate, _: bool = Depends(authorization)):
    valid_player = Player.model_validate(player)
    task = create_player_task(valid_player)

    return task

@router.get('/rankings', response_model=list[Rank])
async def get_rankings(_: bool = Depends(authorization)):
    with Session(engine) as session:
        ranking = session.exec(select(Rank)).all()
        return ranking
    
@router.post('/rankings')
async def create_ranking(ranking: Rank, _: bool = Depends(authorization)):
    with Session(engine) as session:
        session.add(ranking)
        session.commit()
        session.refresh(ranking)
        return ranking