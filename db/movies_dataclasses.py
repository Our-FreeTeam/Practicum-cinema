import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class UUID:
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Dates:
    created_at: datetime = None
    updated_at: datetime = None


@dataclass
class Filmwork(UUID, Dates):
    title: str = ''
    description: str = ''
    creation_date: datetime = None
    type: str = ''
    file_path: str = ''
    rating: float = field(default=0.0)

    def __post_init__(self):
        if self.description is None:
            self.description = ''
        if self.rating is None:
            self.rating = 0
        if self.type is None:
            self.type = ''
        if self.file_path is None:
            self.file_path = ''


@dataclass
class Genre(UUID, Dates):
    name: str = ''
    description: str = ''

    def __post_init__(self):
        if self.description is None:
            self.description = ''


@dataclass
class Person(UUID, Dates):
    full_name: str = ''


@dataclass
class GenreFilmwork(UUID):
    created_at: datetime = None
    film_work_id: uuid = None
    genre_id: uuid = None


@dataclass
class PersonFilmWork(UUID):
    created_at: datetime = None
    film_work_id: uuid = None
    person_id: uuid = None
    role: str = ''
