from abc import ABC, abstractmethod
from collections import defaultdict

import psycopg2
from etl_models import (Genre, Movie, Person, PersonEtl, PersonMovieList,
                        PreparedMovie, PreparedPersonForMovie)
from sql import sql_genres, sql_movies, sql_persons
from sender.src.utils import log
from sender.src.utils import backoff


class AbstractPostgresExtractor(ABC):
    @abstractmethod
    def extract_any(self, last_modified, model_name, logger=None):
        pass


class PostgresExtractor:
    def __init__(self, connection, model, query: str, batch_size: int = 100):
        self.conn = connection
        self.batch_size = batch_size
        self.model = model
        self.query = query

    @log
    @backoff(exception=psycopg2.OperationalError)
    def extract_data(self, last_modified, logger=None):
        with self.conn.cursor() as curs:
            curs.execute(self.query, (last_modified,))
            items = curs.fetchmany(self.batch_size)
        return [self.model(**item) for item in items]

    def transform_data(self, data: list):
        return data

    @log
    def get_data(self, last_modified, logger=None):
        data = self.extract_data(last_modified)
        return self.transform_data(data)


class MovieExtractor(PostgresExtractor):
    def __init__(self, connection, batch_size: int = 100):
        self.conn = connection
        self.batch_size = batch_size
        self.model = Movie
        self.query = sql_movies.sql

    @log
    def transform_data(self, data: list[Movie], logger=None):
        def get_names(name_list: list[PreparedPersonForMovie] = []):
            return [person.name for person in name_list]

        movies = []
        for movie in data:
            new_movie = PreparedMovie(uuid=movie.uuid,
                                      imdb_rating=movie.imdb_rating,
                                      genre=movie.genre,
                                      title=movie.title,
                                      description=movie.description,
                                      modified=movie.modified)
            if movie.persons:
                for person in movie.persons:
                    match person.person_role:
                        case 'director':
                            new_movie.director.append(person.person_name)
                        case 'actor':
                            new_movie.actors.append(PreparedPersonForMovie(uuid=person.person_id,
                                                                           name=person.person_name))
                        case 'writer':
                            new_movie.writers.append(PreparedPersonForMovie(uuid=person.person_id,
                                                                            name=person.person_name))
            new_movie.actors_names = get_names(new_movie.actors)
            new_movie.writers_names = get_names(new_movie.writers)

            movies.append(new_movie)
        return movies


class GenreExtractor(PostgresExtractor):
    def __init__(self, connection, batch_size: int = 100):
        self.conn = connection
        self.batch_size = batch_size
        self.model = Genre
        self.query = sql_genres.sql


class PersonExtractor(PostgresExtractor):
    def __init__(self, connection, batch_size: int = 100):
        self.conn = connection
        self.batch_size = batch_size
        self.model = Person
        self.query = sql_persons.sql

    @log
    def transform_data(self, data: list[Person], logger=None):
        persons = []
        for person in data:
            new_person = PersonEtl(uuid=person.uuid,
                                   full_name=person.full_name,
                                   modified=person.modified)
            if person.films:
                films = defaultdict(list)
                for film in person.films:
                    films[film.uuid].append(film.roles)
                new_person.films = [PersonMovieList(uuid=k, roles=v) for k, v in films.items()]
            persons.append(new_person)
        return persons
