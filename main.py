from flask import Flask, render_template, redirect, abort, request, jsonify, make_response, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session

from functions import *

from forms.loginform import RegisterForm, LoginForm
from forms.small_forms import *
from data.users import User
from data.watchlists import Watchlist
from data.film_comments import FilmComments
from data.saved_films import SavedFilm
from data.film_rating import FilmRating


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key' # позже нужен дургой ключ
#api = Api(app)

#инициализация LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/shows/page1")

@app.route('/')
@app.route('/auth/join', methods=['GET', 'POST']) # регистрация
def join():
    form = RegisterForm()
    if form.validate_on_submit():
        #проверки
        if not is_valid_email(form.email.data):
            return render_template('register2.html', form=form, message='Invalid email address')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register2.html', form=form, message='A user with this email exists')
        if form.password.data != form.password_confirm.data:
            return render_template('register2.html', form=form, message="The entered passwords don't match")
        # добавление пользователя
        user = User(
            email=form.email.data,
            username=form.username.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        # добавление дефолтных значений
        user_id = db_sess.query(User.id).filter(User.email == user.email).first()[0]
        watched_list = Watchlist(
            title='История просмотров',
            type='public',
            user_id=user_id
        )
        watchlist = Watchlist(
            title='Watchlist',
            type='public',
            description='Фильмы, шоу, сериалы, которые я планирую посмотреть.',
            user_id=user_id
        )
        recommendations = Watchlist(
            title='Рекомендации',
            type='public',
            description='Лучшие телешоу и фильмы, которые я рекомендую вам посмотреть.',
            user_id=user_id
        )
        db_sess.add(watched_list)
        db_sess.add(watchlist)
        db_sess.add(recommendations)
        db_sess.commit()
        return redirect('/auth/signin')
    return render_template('register.html', form=form)


@app.route('/auth/signin', methods=['GET', 'POST']) # вход
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect('/shows/page1')
        return render_template('sign_in2.html', form=form, message='Incorrect login or password')
    return render_template('sign_in.html', form=form)

@app.route('/<film_type>/page<int:page>', methods=['GET', 'POST']) # шоу, тренды
def shows(film_type, page):
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/search/{form.search_query.data}/page1')
    json_request = kinopoisk_request(film_type, page)
    final_page = json_request['totalPages']
    resolution1 = False if page == 1 else True
    resolution2 = False if page == final_page else True
    films = json_request['items']
    return render_template('shows.html', films=films, page=page, 
                           resolution1=resolution1, resolution2=resolution2, film_type=film_type, search_form=form)

@app.route('/search/<squery>/page<int:page>', methods=['POST', 'GET'])
def search(squery, page):
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/search/{form.search_query.data}/page1')
    json_request = search_query(squery, page)
    final_page = json_request['pagesCount']
    resolution1 = False if page == 1 else True
    resolution2 = False if page == final_page else True
    films = json_request['films']
    return render_template('search_html.html', films=films, page=page, 
                           resolution1=resolution1, resolution2=resolution2, film_type=squery, search_form=form)


@app.route('/watched', methods=['POST'])
def watched():
    db_sess = db_session.create_session()
    film = SavedFilm(
        user_id=current_user.id,
        film_id=request.form['movie_id'],
        watchlist_id=db_sess.query(Watchlist.id).filter(Watchlist.user_id == current_user.id and Watchlist.title == 'История просмотров').first()[0]
    )
    if db_sess.query(SavedFilm).filter(SavedFilm.film_id == film.film_id and SavedFilm.watchlist_id == film.watchlist_id and SavedFilm.user_id == current_user.id).first() is None:
        db_sess.add(film)
        db_sess.commit()
    return redirect(request.referrer)

@app.route('/recommendation', methods=['POST'])
def recommendation():
    db_sess = db_session.create_session()
    film = SavedFilm(
        user_id=current_user.id,
        film_id=request.form['movie_id'],
        watchlist_id=db_sess.query(Watchlist.id).filter(Watchlist.user_id == current_user.id, Watchlist.title == 'Рекомендации').first()[0]
    )
    if db_sess.query(SavedFilm).filter(SavedFilm.film_id == film.film_id, SavedFilm.watchlist_id == film.watchlist_id, SavedFilm.user_id == current_user.id).first() is None:
        db_sess.add(film)
        db_sess.commit()
    return redirect(request.referrer)

@app.route('/select_list')
def get_options():
    db_sess = db_session.create_session()
    options = db_sess.query(Watchlist.title).filter(Watchlist.title != 'История просмотров', Watchlist.title != 'Рекомендации', Watchlist.user_id == current_user.id)
    options = [tuple(row) for row in options]
    return jsonify({'list': options})

@app.route('/save_movie', methods=['POST'])
def saving_film():
    db_sess = db_session.create_session()
    watchlist_name = request.form['watchlist']
    film_id=request.form['filmId']
    film = SavedFilm(
        user_id=current_user.id,
        film_id=film_id,
        watchlist_id=db_sess.query(Watchlist.id).filter(Watchlist.user_id == current_user.id, Watchlist.title == watchlist_name).first()[0]
    )
    if db_sess.query(SavedFilm).filter(SavedFilm.film_id == film.film_id, SavedFilm.watchlist_id == film.watchlist_id, SavedFilm.user_id == current_user.id).first() is None:
        db_sess.add(film)
        db_sess.commit()
    return redirect(request.referrer)


@app.route('/<film_id>')
def show(film_id):
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/search/{form.search_query.data}/page1')
    json_request = data_about_film(film_id)
    return render_template('film_description.html', data=json_request, search_form=form)

@app.route('/users/<int:id>/history')
def history(id):
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/search/{form.search_query.data}/page1')
    db_sess = db_session.create_session()
    watchlist_id = db_sess.query(Watchlist.id).filter(Watchlist.user_id == current_user.id, Watchlist.title == 'История просмотров').first()
    films = db_sess.query(SavedFilm.film_id).filter(SavedFilm.user_id == current_user.id, SavedFilm.watchlist_id == watchlist_id).all()
    return render_template('search_html.html', films=films, page=1, 
                           resolution1=False, resolution2=False, film_type='no', search_form=form)

def main():
    db_session.global_init("db/films.db")
    app.run()


if __name__ == '__main__':
    main()