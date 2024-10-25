from sqlmodel import Session, select
from db_config import engine
from player.models import Player, Team
from celery.utils.log import get_task_logger

from worker.celery_worker import celery_app

logger = get_task_logger(__name__)


@celery_app.task(trail=True)
def create_team_task(team: Team):
    with Session(engine) as session:
        session.add(team)
        session.commit()
        session.refresh(team)
        return team

@celery_app.task(trail=True)
def create_player_task(player: Player):
    with Session(engine) as session:
        session.add(player)
        session.commit()
        session.refresh(player)
        return player

@celery_app.task(trail=True)
def get_players_task():
    with Session(engine) as session:
        players = session.exec(select(Player)).all()
        return players.dict()
    
@celery_app.task(serializer='json')
def example_task(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))

    return x + y