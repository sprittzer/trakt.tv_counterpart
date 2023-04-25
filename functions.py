import re
import requests


API_KEY = '8c8e1a50-6322-4135-8875-5d40a5420d86'


def is_valid_email(email):
    # Проверка на действительность адреса электронной почты
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
    return re.match(pattern, email) is not None

def kinopoisk_request(film_type, page):
    type_conversion = {'shows': 'TV_SHOW', 'movies': 'FILM', 
                       'serieses': 'TV_SERIES', 'miniserieses': 'MINI_SERIES'}
    url = 'https://kinopoiskapiunofficial.tech/api/v2.2/films'
    params = {
        'order': 'RATING',
        'type': type_conversion[film_type],
        'ratingFrom': 0,
        'ratingTo': 10,
        'yearFrom': 1000,
        'yearTo': 3000,
        'page': page
    }
    headers = {
	"Content-Type": "application/json",
	"X-API-KEY": API_KEY
}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data

def search_query(word, page):
    url = "https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword"
    params = {"keyword": word, "page": page}
    headers = {
	"Content-Type": "application/json",
	"X-API-KEY": API_KEY
}
    data = requests.get(url, params=params, headers=headers).json()
    for movie in data['films']:
        if movie['rating'] != 'null':
            movie['rating'] = float(movie['rating'])
    return data

def data_about_film(film_id):
    url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_id}'
    headers = {
	"Content-Type": "application/json",
	"X-API-KEY": API_KEY
}
    data = requests.get(url, headers=headers).json()
    return data
