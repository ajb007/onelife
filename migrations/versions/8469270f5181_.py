"""empty message

Revision ID: 8469270f5181
Revises: None
Create Date: 2016-04-24 12:29:36.282776

"""

# revision identifiers, used by Alembic.
revision = '8469270f5181'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('account', postgresql.JSON(), nullable=True),
    sa.Column('accountb', postgresql.JSONB(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('king',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('king_flag', sa.Boolean(), nullable=True),
    sa.Column('x', sa.Integer(), nullable=True),
    sa.Column('y', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('objects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('object_type', sa.String(), nullable=True),
    sa.Column('x', sa.Integer(), nullable=True),
    sa.Column('y', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('player', postgresql.JSON(), nullable=True),
    sa.Column('playerb', postgresql.JSONB(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('players')
    op.drop_table('objects')
    op.drop_table('king')
    op.drop_table('accounts')
    ### end Alembic commands ###
