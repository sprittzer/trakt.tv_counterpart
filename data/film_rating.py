import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class FilmRating(SqlAlchemyBase):
    __tablename__ = 'film_rating'

    flim_id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    rating = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user = orm.relationship('User')