"""Initial migration

Revision ID: 270eeb00bf47
Revises: 907aa80a417b
Create Date: 2024-02-11 19:00:51.581442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '270eeb00bf47'
down_revision: Union[str, None] = '907aa80a417b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type_goods', sa.String(), nullable=False),
    sa.Column('teg', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('teg'),
    sa.UniqueConstraint('type_goods')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags')
    # ### end Alembic commands ###
