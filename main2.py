import requests
API_KEY = '8c8e1a50-6322-4135-8875-5d40a5420d86'
url = "https://kinopoiskapiunofficial.tech/api/v2.2/films?order=RATING&type=TV_SHOW&ratingFrom=0&ratingTo=10&yearFrom=1000&yearTo=3000&page"

headers = {
	"Content-Type": "application/json",
	"X-API-KEY": API_KEY
}

response = requests.request("GET", url, headers=headers)

print(response.json())