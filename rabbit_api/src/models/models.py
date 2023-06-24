import uuid

from sqlalchemy import String, BOOLEAN, Text, Column, text
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import Base


class Template(Base):
    __tablename__ = "templates"

    __table_args__ = {"schema": "content"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event = Column(String)
    instant_event = Column(BOOLEAN)
    title = Column(String)
    text = Column(Text)
