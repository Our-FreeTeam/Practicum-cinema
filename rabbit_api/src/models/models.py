import sqlalchemy

from db.postgres import Base


class Template(Base):
    __tablename__ = "templates"

    __table_args__ = {'schema': 'content'}

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    event = sqlalchemy.Column(sqlalchemy.String)
    instant_event = sqlalchemy.Column(sqlalchemy.BOOLEAN)
    title = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.Text)
