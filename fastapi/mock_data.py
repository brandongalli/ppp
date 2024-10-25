import random
from datetime import datetime, timedelta
from faker import Faker
from sqlmodel import Session, select

from game.models import Game, Stadium
from player.models import Player, Team, PositionChoices
from db_config import engine

# Initialize Faker for generating random data
fake = Faker()

def create_teams(session: Session, num_teams: int = 32):
    """
    Creates a specified number of teams with unique names and logos.

    Parameters:
    - session: The active SQLModel session.
    - num_teams: The number of teams to create (default is 32).

    Returns:
    - A list of created Team objects.
    """
    teams = []
    for _ in range(num_teams):
        team = Team(
            name=f"{fake.city()} {fake.word()}s",
            logo_uri=f"{fake.word()}.png"
        )
        session.add(team)
        session.commit()  # Commit each team to ensure IDs are available for players
        teams.append(team)
    return teams

def create_stadiums(session: Session, num_stadiums: int = 32):
    """
    Creates a specified number of stadiums with random names and locations.

    Parameters:
    - session: The active SQLModel session.
    - num_stadiums: The number of stadiums to create (default is 32).

    Returns:
    - A list of created Stadium objects.
    """
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
    """
    Creates a specified number of players for each team with random attributes.

    Parameters:
    - session: The active SQLModel session.
    - teams: A list of Team objects to assign players to.
    - num_players_per_team: The number of players per team (default is 20).
    """
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
        session.commit()  # Commit after each team’s players are added

def create_games(session: Session, teams, stadiums, num_games_per_team: int = 10):
    """
    Creates a specified number of games for each team with random dates, scores, opponents, and stadiums.

    Parameters:
    - session: The active SQLModel session.
    - teams: A list of Team objects to schedule games for.
    - stadiums: A list of Stadium objects to host games.
    - num_games_per_team: The number of games per team (default is 10).
    """
    for team in teams:
        for _ in range(num_games_per_team):
            opponent = random.choice([t for t in teams if t.id != team.id])  # Avoid team playing against itself
            stadium = random.choice(stadiums)
            
            # Generate random game details
            game_date = fake.date_between(start_date='-2y', end_date='today')
            home_team_score = random.randint(0, 40)
            away_team_score = random.randint(0, 40)
            
            # Create and add the game record
            game = Game(
                date=game_date,
                home_team_id=team.id,
                away_team_id=opponent.id,
                home_team_score=home_team_score,
                away_team_score=away_team_score,
                stadium_id=stadium.id
            )
            session.add(game)
        session.commit()  # Commit after adding each team’s games

def populate_database():
    """
    Populates the database with teams, stadiums, players, and games.

    This function initializes the database by creating teams, stadiums, players, and games.
    It uses Faker to generate random values for names, locations, scores, etc.
    """
    with Session(engine) as session:
        # Generate and populate teams, stadiums, players, and games
        teams = create_teams(session)
        stadiums = create_stadiums(session)
        create_players(session, teams)
        create_games(session, teams, stadiums)
