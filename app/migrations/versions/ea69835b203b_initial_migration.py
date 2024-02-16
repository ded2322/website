"""Initial migration

Revision ID: ea69835b203b
Revises: a16cb3622ecd
Create Date: 2024-02-09 09:42:34.004641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea69835b203b'
down_revision: Union[str, None] = 'a16cb3622ecd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_email_key', 'user', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('user_email_key', 'user', ['email'])
    # ### end Alembic commands ###
