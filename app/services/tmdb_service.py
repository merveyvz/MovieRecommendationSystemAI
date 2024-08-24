import aiohttp
import asyncio
import requests
from app.config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE_URL
from app.models import Movie
from app.database import SessionLocal
from datetime import datetime
import time


# Global variable to store popular movies
popular_movies_cache = []
popular_movies_last_update = 0
CACHE_DURATION = 3600  # 1 hour


def get_genres():
    genre_url = f"{TMDB_BASE_URL}/genre/movie/list"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(genre_url, params=params)
    data = response.json()
    return {genre['id']: genre['name'] for genre in data['genres']}


genres_dict = get_genres()


def get_movie_details(movie_id_or_title):
    if isinstance(movie_id_or_title, int) or movie_id_or_title.isdigit():
        details_url = f"{TMDB_BASE_URL}/movie/{movie_id_or_title}"
        params = {"api_key": TMDB_API_KEY}
    else:
        search_url = f"{TMDB_BASE_URL}/search/movie"
        params = {"api_key": TMDB_API_KEY, "query": movie_id_or_title}
        search_response = requests.get(search_url, params=params)
        search_data = search_response.json()
        if not search_data['results']:
            return None
        movie_id = search_data['results'][0]['id']
        details_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        params = {"api_key": TMDB_API_KEY}

    response = requests.get(details_url, params=params)
    movie = response.json()

    return {
        "title": movie["title"],
        "genre": ", ".join([genres_dict.get(genre['id'], "Unknown") for genre in movie["genres"]]),
        "release_date": movie["release_date"],
        "rating": movie["vote_average"],
        "overview": movie["overview"],
        "poster_path": f"{TMDB_IMAGE_BASE_URL}{movie['poster_path']}" if movie['poster_path'] else None,
    }


async def get_movie_details_async(session, movie_id_or_title):
    if isinstance(movie_id_or_title, int) or movie_id_or_title.isdigit():
        details_url = f"{TMDB_BASE_URL}/movie/{movie_id_or_title}"
        params = {"api_key": TMDB_API_KEY}
    else:
        search_url = f"{TMDB_BASE_URL}/search/movie"
        params = {"api_key": TMDB_API_KEY, "query": movie_id_or_title}
        async with session.get(search_url, params=params) as search_response:
            search_data = await search_response.json()
            if not search_data['results']:
                return None
            movie_id = search_data['results'][0]['id']
            details_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
            params = {"api_key": TMDB_API_KEY}

    async with session.get(details_url, params=params) as response:
        movie = await response.json()

    return {
        "title": movie["title"],
        "genre": ", ".join([genres_dict.get(genre['id'], "Unknown") for genre in movie["genres"]]),
        "release_date": movie["release_date"],
        "rating": movie["vote_average"],
        "overview": movie["overview"],
        "poster_path": f"{TMDB_IMAGE_BASE_URL}{movie['poster_path']}" if movie['poster_path'] else None,
    }


async def fetch_popular_movies():
    global popular_movies_cache, popular_movies_last_update
    async with aiohttp.ClientSession() as session:
        popular_url = f"{TMDB_BASE_URL}/movie/popular"
        params = {"api_key": TMDB_API_KEY}
        async with session.get(popular_url, params=params) as response:
            data = await response.json()

        tasks = [get_movie_details_async(session, movie["id"]) for movie in data["results"][:14]]
        popular_movies_cache = await asyncio.gather(*tasks)
        popular_movies_last_update = time.time()


def get_popular_movies():
    global popular_movies_cache, popular_movies_last_update
    current_time = time.time()

    if not popular_movies_cache or (current_time - popular_movies_last_update) > CACHE_DURATION:
        asyncio.run(fetch_popular_movies())

    return popular_movies_cache


def update_popular_movies():
    db = SessionLocal()
    popular_movies = get_popular_movies()

    for movie_data in popular_movies:
        movie = Movie(
            title=movie_data["title"],
            genre=movie_data["genre"],
            release_date=datetime.strptime(movie_data["release_date"], "%Y-%m-%d").date(),
            rating=movie_data["rating"],
            overview=movie_data["overview"],
            poster_path=movie_data["poster_path"],
        )
        db.add(movie)

    db.commit()
    db.close()