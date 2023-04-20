import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True, index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    display_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    birthday = sqlalchemy.Column(sqlalchemy.Date)
    gender = sqlalchemy.Column(sqlalchemy.String, default='Unknown')
    private = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    film_rating = orm.relationship('FilmRating', back_populates='user')
    film_comments = orm.relationship('FilmComments', back_populates='user')