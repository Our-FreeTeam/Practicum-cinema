"""Fixes

Revision ID: 64hpjju74ddr
Revises: 
Create Date: 2023-07-07 23:15:01.648392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.dialects import postgresql

revision = '64hpjju74ddr'
down_revision = 'a070fecf1016'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('alter table subscription add column is_repeatable boolean')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('alter table subscription drop column is_repeatable')
    # ### end Alembic commands ###
