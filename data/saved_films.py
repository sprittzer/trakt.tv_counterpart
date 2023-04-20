import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class SavedFilm(SqlAlchemyBase):
    __tablename__ = 'saved_films'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    watchlist_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("watchlists.id"))
    watchlist = orm.relationship('Watchlist')