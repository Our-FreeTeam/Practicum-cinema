import datetime

from dateutil.relativedelta import relativedelta

from sqlalchemy import (TIMESTAMP, Column, DateTime, Enum, ForeignKey, Index,
                        Integer, String, func, text, BOOLEAN, DECIMAL)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, declarative_mixin

Base = declarative_base()

DATE_DIR = {
    'month': datetime.datetime.today() + relativedelta(months=1),
    'year': datetime.datetime.today() + relativedelta(year=1),
}


@declarative_mixin
class TimeStapleMixin:
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())


@declarative_mixin
class UUIDMixin:
    id = Column(UUID, primary_key=True, server_default=text('uuid_generate_v4()'))


class Genre(Base, UUIDMixin, TimeStapleMixin):
    __tablename__ = 'genre'
    __table_args__ = {'schema': 'content'}

    name = Column(String(255))
    description = Column(String, nullable=True)


class Person(Base, UUIDMixin, TimeStapleMixin):
    __tablename__ = 'person'
    __table_args__ = {'schema': 'content'}

    full_name = Column(String(255), unique=True)


class Filmwork(Base, UUIDMixin, TimeStapleMixin):
    __tablename__ = 'film_work'
    __table_args__ = {'schema': 'content'}

    title = Column(String(255))
    description = Column(String, nullable=True)
    creation_date = Column(DateTime, nullable=True)
    file_path = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)
    type = Column(Enum('movie', 'tv_show', name='MovieType'), default='movie')


class PersonFilmwork(Base, UUIDMixin):
    __tablename__ = 'person_film_work'
    __table_args__ = (
        Index('idxu_person_filmwork', 'film_work_id', 'person_id', 'role'),
        {'schema': 'content'})
    film_work_id = Column(UUID, ForeignKey('content.film_work.id', ondelete='CASCADE'))
    person_id = Column(UUID, ForeignKey('content.person.id', ondelete='CASCADE'))
    created_at = Column(TIMESTAMP, default=func.now())
    role = Column(Enum('actor', 'director', 'writer', name='RoleTypes'), nullable=True)


class GenreFilmwork(Base, UUIDMixin):
    __tablename__ = 'genre_film_work'
    __table_args__ = (
        Index('idxu_genre_film_work', 'film_work_id', 'genre_id', unique=True),
        {'schema': 'content'})

    film_work_id = Column(UUID, ForeignKey('content.film_work.id', ondelete='CASCADE'))
    genre_id = Column(UUID, ForeignKey('content.genre.id', ondelete='CASCADE'))
    created_at = Column(TIMESTAMP, default=func.now())


class Subscriptions(Base, UUIDMixin):
    __tablename__ = 'subscriptions'
    __table_args__ = (
        Index('user_id', unique=True),
        {'schema': 'content'})

    user_id = Column(UUID, ForeignKey('content.user.id', ondelete='CASCADE'))
    start_date = Column(TIMESTAMP, default=func.now())
    end_date = Column(TIMESTAMP, default=DATE_DIR['year'])
    subscription_type = Column(String, nullable=True)
    is_active = Column(BOOLEAN)


class Payments(Base, UUIDMixin, TimeStapleMixin):
    __tablename__ = 'payments'
    __table_args__ = (
        Index('user_id', 'subscription_id', unique=True),
        {'schema': 'content'})

    user_id = Column(UUID, ForeignKey('content.user.id', ondelete='CASCADE'))
    subscription_id = Column(UUID, ForeignKey('content.subscription.id', ondelete='CASCADE'))
    payment_amount = Column(DECIMAL(precision=None))
    payment_status = Column(String, nullable=True)
    external_payment_id = Column(String, nullable=True)


class Refunds(Base, UUIDMixin, TimeStapleMixin):
    __tablename__ = 'refunds'
    __table_args__ = (
        Index('payment_id', unique=True),
        {'schema': 'content'})

    payment_id = Column(UUID, ForeignKey('content.payment.id', ondelete='CASCADE'))
    refund_amount = Column(DECIMAL(precision=None))
    refund_status = Column(String, nullable=True)
    external_refund_id = Column(String, nullable=True)
