from flask import Flask, render_template, redirect, abort, request, jsonify, make_response
#from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
#import users_resource, jobs_resource
#from flask_restful import reqparse, abort, Api, Resource
#from forms.user import RegisterForm
#from forms.loginform import LoginForm
#from forms.jobs import JobsForm
#from forms.departments import DepartmentsForm
#from data.users import User
#from data.jobs import Jobs
#from data.departments import Department


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key' # позже нужен дургой ключ
#api = Api(app)

@app.route('/')
def index():
    return render_template('index.html', title='Главная страница')

@app.route('/auth/join') # регистрация
def join():
    return 'Регистрация'

@app.route('/auth/signin') # вход
def signin():
    return 'Вход'

@app.route('/shows/trending') # шоу, тренды
def shows_trending():
    return 'Тренды для шоу'

@app.route('/shows/popular')
def shows_popular():
    return 'Популярные шоу'

@app.route('/shows/recommended')
def shows_recommended():
    return 'Рекомендуемые шоу'

@app.route('/shows/anticipated')
def shows_anticipated():
    return 'Ожидаемые шоу'

def main():
    db_session.global_init("db/films.db")
    app.run()


if __name__ == '__main__':
    main()
    