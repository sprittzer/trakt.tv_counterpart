from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired


class AddingFilmToWatched(FlaskForm):
    film_id = StringField(validators=[DataRequired()])
    watchlist_id = IntegerField(validators=[DataRequired()])


class FormButtons(FlaskForm):
    film_id = StringField()
    watched_btn = SubmitField()


class SearchForm(FlaskForm):
    search_query = StringField(validators=[DataRequired()])
    search_btn = SubmitField('->')