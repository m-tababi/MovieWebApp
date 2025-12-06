from flask import Flask
from models import db
from DataManager import DataManager
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "data", "movies.sqlite3")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    dm = DataManager()
#    dm.add_user("Mo")
#    dm.add_movie("Jay Kelly")

    users = dm.get_users()
    for u in users:
        print(u)

    movies = dm.get_movies()
    for m in movies:
        print(m)