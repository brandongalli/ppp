"""Updated relationships

Revision ID: e5d4ac83048b
Revises: d37665039a76
Create Date: 2024-10-25 16:16:37.855544

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'e5d4ac83048b'
down_revision: Union[str, None] = 'd37665039a76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('game_ibfk_1', 'game', type_='foreignkey')
    op.drop_constraint('game_ibfk_2', 'game', type_='foreignkey')
    op.drop_column('game', 'away_team_id')
    op.drop_column('game', 'home_team_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('home_team_id', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('game', sa.Column('away_team_id', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('game_ibfk_2', 'game', 'team', ['home_team_id'], ['id'])
    op.create_foreign_key('game_ibfk_1', 'game', 'team', ['away_team_id'], ['id'])
    # ### end Alembic commands ###