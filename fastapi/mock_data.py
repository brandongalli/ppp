import random
from datetime import datetime, timedelta
from faker import Faker
from sqlmodel import Session, select

from game.models import Game, Stadium
from player.models import Player, Team, PositionChoices
from db_config import engine  # Import your SQLAlchemy engine

fake = Faker()

def create_teams(session: Session, num_teams: int = 32):
    teams = []
    for _ in range(num_teams):
        team = Team(
            name=f"{fake.city()} {fake.word()}s",
            logo_uri=f"{fake.word()}.png"
        )
        session.add(team)
        session.commit()
        teams.append(team)
    return teams

def create_stadiums(session: Session, num_stadiums: int = 32):
    stadiums = []
    for _ in range(num_stadiums):
        stadium = Stadium(
            name=f"{fake.city()} Stadium",
            location=fake.city()
        )
        session.add(stadium)
        session.commit()
        stadiums.append(stadium)
    return stadiums

def create_players(session: Session, teams, num_players_per_team: int = 20):
    for team in teams:
        for _ in range(num_players_per_team):
            player = Player(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                team_id=team.id,
                position=random.choice(list(PositionChoices)),
                number=random.randint(1, 99),
                height=round(random.uniform(5.5, 7.0), 2),
                weight=random.randint(150, 350),
                birth_year=random.randint(1980, 2000),
                debut_year=random.randint(2005, 2022),
                college=fake.company(),
                bio=fake.text()
            )
            session.add(player)
        session.commit()

def create_games(session: Session, teams, stadiums, num_games_per_team: int = 10):
    for team in teams:
        for _ in range(num_games_per_team):
            # Randomly select opponent and stadium
            opponent = random.choice([t for t in teams if t.id != team.id])
            stadium = random.choice(stadiums)
            
            # Randomize date and score
            game_date = fake.date_between(start_date='-2y', end_date='today')
            home_team_score = random.randint(0, 40)
            away_team_score = random.randint(0, 40)
            
            # Create the game record
            game = Game(
                date=game_date,
                home_team_id=team.id,
                away_team_id=opponent.id,
                home_team_score=home_team_score,
                away_team_score=away_team_score,
                stadium_id=stadium.id
            )
            session.add(game)
        session.commit()

def populate_database():
    with Session(engine) as session:
        teams = create_teams(session)
        stadiums = create_stadiums(session)
        create_players(session, teams)
        create_games(session, teams, stadiums)
