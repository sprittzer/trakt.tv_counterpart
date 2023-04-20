import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Watchlist(SqlAlchemyBase):
    __tablename__ = 'watchlists'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    default_sort = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    saved_films = orm.relationship("SavedFilm", back_populates='watchlist')
