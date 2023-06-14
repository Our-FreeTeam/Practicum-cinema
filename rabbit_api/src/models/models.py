import sqlalchemy
from sqlalchemy import Boolean, Column, Integer, String, Table, Text

from db.postgres import Base, metadata


class Template(Base):
    __tablename__ = "templates"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    event = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    instant_event = sqlalchemy.Column(sqlalchemy.BOOLEAN)
    title = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.Text)


template = Table(
    "templates",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("event", String, unique=True, index=True),
    Column("instant_event", Boolean),
    Column("title", String),
    Column("text", Text),
)
