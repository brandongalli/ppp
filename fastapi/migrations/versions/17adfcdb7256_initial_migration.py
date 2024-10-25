"""Initial migration

Revision ID: 17adfcdb7256
Revises: 
Create Date: 2024-10-25 15:41:49.824259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '17adfcdb7256'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stadium',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('location', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stadium_name'), 'stadium', ['name'], unique=True)
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('logo_uri', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_team_name'), 'team', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('home_team_score', sa.Integer(), nullable=False),
    sa.Column('away_team_score', sa.Integer(), nullable=False),
    sa.Column('stadium_id', sa.Integer(), nullable=False),
    sa.Column('home_team_id', sa.Integer(), nullable=False),
    sa.Column('away_team_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['away_team_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['home_team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('player',
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('position', sa.Enum('Quarterback', 'Center', 'RunningBack', 'FullBack', 'WideReceiver', 'TightEnd', 'LeftGuard', 'LeftTackle', 'Safety', 'DefensiveTackle', 'DefensiveEnd', 'LineBacker', 'CornerBack', 'Kicker', 'Putner', name='positionchoices'), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('height', sa.Float(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.Column('birth_year', sa.Integer(), nullable=False),
    sa.Column('debut_year', sa.Integer(), nullable=False),
    sa.Column('college', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('bio', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rank',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.Column('ranking_type', sa.Enum('WorldRanking', 'GameRanking', name='rankingchoices'), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['player.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rank')
    op.drop_table('player')
    op.drop_table('game')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_team_name'), table_name='team')
    op.drop_table('team')
    op.drop_index(op.f('ix_stadium_name'), table_name='stadium')
    op.drop_table('stadium')
    # ### end Alembic commands ###
