from fastapi import Depends, APIRouter
from sqlmodel import Session, select
from auth.provider import authorization

from db_config import engine
from player.models import Player


router = APIRouter()

@router.get('/players', response_model=list[Player])
async def get_players(_: bool = Depends(authorization)):
    with Session(engine) as session:
        songs = session.exec(select(Player)).all()
        return songs
    
@router.post('/players', response_model=Player)
async def create_player(player: Player, _: bool = Depends(authorization)):
    with Session(engine) as session:
        session.add(player)
        session.commit()
        session.refresh(player)
        return player