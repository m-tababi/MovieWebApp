from models import db, User, Movie
from dotenv import load_dotenv
import requests
import os


load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_URL = "https://www.omdbapi.com/"


class DataManager:
    def add_user(self, name: str):
        new_user = User(name = name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def add_movie(self, title: str, user_id: int):
        if not OMDB_API_KEY:
            print("NO OMDB_API_KEY")
            return None

        try:
            resp = requests.get(OMDB_URL, params={"t": title, "apikey": OMDB_API_KEY}, timeout=10)
            data = resp.json()
        except Exception as e:
            print("OMDb Request-Error:", e)
            return None

        if data.get("Response") != "True":
            print(f"OMDb: {data.get('Error', 'no match')}")
            return None

        imdb_rating = data.get("imdbRating")
        try:
            rating = float(imdb_rating) if imdb_rating not in (None, "N/A", "") else 0.0
        except ValueError:
            rating = 0.0

        try:
            year = int(data.get("Year"))
        except (TypeError, ValueError):
            year = 0

        poster = data.get("Poster")
        if not poster or poster == "N/A":
            poster = None
        new_movie = Movie(title=data.get("Title") or title, year=year, rating= rating, poster=poster, user_id=user_id)
        db.session.add(new_movie)
        db.session.commit()
        return new_movie

    def get_users(self):
        return User.query.all()

    def get_movies(self):
        return Movie.query.all()

    def get_movies_by_user(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def update_movie(self, movie_id, new_title):
        movie_to_update = Movie.query.get(movie_id)

        if movie_to_update is None:
            return False

        movie_to_update.title = new_title
        db.session.commit()
        return True

    def delete_movie(self, movie_id):
        movie_to_delete = Movie.query.get(movie_id)

        if movie_to_delete is None:
            return False

        db.session.delete(movie_to_delete)
        db.session.commit()
        return True
