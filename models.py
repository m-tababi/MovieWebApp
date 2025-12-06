from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    movies = db.relationship("Movie", backref="user", lazy=True)

    def __str__(self):
        return f"User(id={self.user_id}, name='{self.name}')"

class Movie(db.Model):
    __tablename__= "movies"

    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float)
    poster = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __str__(self):
        return f"Movie(id={self.movie_id}, title='{self.title}', year={self.year}, rating={self.rating})"