from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField(validators=[DataRequired()])
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    password_confirm = PasswordField(validators=[DataRequired()])
    submit = SubmitField('LOG IN')


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('LOG IN')