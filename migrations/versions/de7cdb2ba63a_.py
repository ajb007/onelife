"""empty message

Revision ID: de7cdb2ba63a
Revises: 12bbeec762fe
Create Date: 2016-03-19 20:04:07.878044

"""

# revision identifiers, used by Alembic.
revision = 'de7cdb2ba63a'
down_revision = '12bbeec762fe'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('accountb', postgresql.JSONB(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('account', 'accountb')
    ### end Alembic commands ###