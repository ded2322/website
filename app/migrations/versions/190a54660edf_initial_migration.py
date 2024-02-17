"""Initial migration

Revision ID: 190a54660edf
Revises: 
Create Date: 2024-02-17 12:37:45.170123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '190a54660edf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tag', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tag')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=True),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('goods',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('basket',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_goods', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_goods'], ['goods.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('stars', sa.Integer(), nullable=False),
    sa.Column('id_goods', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_goods'], ['goods.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    op.drop_table('basket')
    op.drop_table('goods')
    op.drop_table('user')
    op.drop_table('tags')
    # ### end Alembic commands ###
