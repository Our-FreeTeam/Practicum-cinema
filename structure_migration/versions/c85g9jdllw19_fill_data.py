"""fill_data

Revision ID: c85g9jdllw19
Revises: 
Create Date: 2023-03-08 14:01:03.635129

"""
from alembic import op
from sqlalchemy import DDL

from src.db import insert_film_work
from src.db import insert_genre
from src.db import insert_genre_film_work
from src.db import insert_person
from src.db import insert_person_film_work

# revision identifiers, used by Alembic.
revision = 'c85g9jdllw19'
down_revision = 'b8b5ec5f1e13'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(insert_genre)
    op.execute(insert_person)
    op.execute(insert_film_work)
    op.execute(insert_genre_film_work)
    op.execute(insert_person_film_work)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    drop_schema = DDL('''
        delete from person_film_work;
        delete from genre_film_work;
        delete from person;
        delete from genre;
        delete from film_work;
    ''')
    drop_schema(target=None, bind=op.get_bind())
    # ### end Alembic commands ###
