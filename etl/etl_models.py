from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MoviePerson(BaseModel):
    person_id: UUID
    person_name: str
    person_role: str


class PersonMovie(BaseModel):
    uuid: UUID
    roles: str


class Person(BaseModel):
    uuid: UUID
    full_name: str
    modified: datetime
    films: list[PersonMovie]


class PersonMovieList(BaseModel):
    uuid: UUID
    roles: list[str]


class PersonEtl(BaseModel):
    uuid: UUID
    full_name: str
    modified: datetime
    films: list[PersonMovieList] = []


class PreparedGenre(BaseModel):
    uuid: UUID
    name: str


class Movie(BaseModel):
    uuid: UUID
    imdb_rating: float
    genre: list[PreparedGenre] = []
    title: str
    description: str
    persons: list[MoviePerson] = []
    modified: datetime


class Genre(BaseModel):
    uuid: UUID
    name: str
    description: str
    modified: datetime


class PreparedPersonForMovie(BaseModel):
    uuid: UUID
    name: str


class PreparedMovie(BaseModel):
    uuid: UUID
    imdb_rating: float
    genre: list[PreparedGenre] = []
    title: str
    description: str
    director: list[str] = []
    actors_names: list[str] = []
    writers_names: list[str] = []
    actors: list[PreparedPersonForMovie] = []
    writers: list[PreparedPersonForMovie] = []
    modified: datetime | None
