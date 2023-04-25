import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class SavedFilm(SqlAlchemyBase):
    __tablename__ = 'saved_films'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    film_id = sqlalchemy.Column(sqlalchemy.String)
    watchlist_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("watchlists.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    watchlist = orm.relationship('Watchlist')