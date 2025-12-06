from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User
from DataManager import DataManager
import os

app = Flask(__name__)

# Secret key for sessions / flash messages
app.secret_key = "super_geheimer_schluessel_123"

# Build database path
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "data", "movies.sqlite3")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
dm = DataManager()


# ---------------------------------------------------------------------------
# User routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """
    Homepage:
    Displays all users and includes a form to create a new user.
    """
    users = dm.get_users()
    return render_template("index.html", users=users)


@app.route("/users")
def list_users():
    """
    Displays all users in a table.
    """
    users = dm.get_users()
    return render_template("users.html", users=users)


@app.route("/create_user", methods=["POST"])
def create_user():
    """
    Creates a new user.
    Reads the value from the form field 'name'.
    """
    name = (request.form.get("name") or "").strip()

    if not name:
        flash("Bitte gib einen Namen ein.", "error")
        return redirect(url_for("index"))

    users = dm.get_users()
    existing_users = [m.name.lower() for m in users]

    if name.strip().lower() in existing_users:
        flash("Der User existiert bereits.", "error")
        return redirect(url_for("index"))

    dm.add_user(name)
    flash(f"User '{name}' wurde angelegt.", "success")
    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# Movie routes (global + per user)
# ---------------------------------------------------------------------------

@app.route("/movies")
def list_movies():
    """
    Shows all movies (without user context).
    """
    movies = dm.get_movies()
    return render_template("movies.html", movies=movies, user=None)


@app.route("/users/<int:user_id>")
def get_movies(user_id):
    """
    Shows all movies belonging to a specific user.
    """
    user = User.query.get_or_404(user_id)
    movies = dm.get_movies_by_user(user_id)
    return render_template("movies.html", movies=movies, user=user)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """
    Adds a movie to a specific user.
    This calls dm.add_movie(), which fetches metadata from the OMDb API.
    """
    raw_title = request.form.get("title") or ""
    title = " ".join(raw_title.split())  # trim + remove double spaces

    if not title:
        flash("Bitte gib einen Filmtitel ein.", "error")
        return redirect(url_for("get_movies", user_id=user_id))

    # Duplicate check (case-insensitive)
    user_movies = dm.get_movies_by_user(user_id)
    existing_titles = [m.title.lower() for m in user_movies]

    if title.strip().lower() in existing_titles:
        flash("Der Film existiert bereits für diesen User.", "error")
        return redirect(url_for("get_movies", user_id=user_id))

    new_movie = dm.add_movie(title, user_id)

    if new_movie is None:
        flash("Film konnte nicht gefunden werden. Bitte überprüfe den Titel.", "error")
        return redirect(url_for("get_movies", user_id=user_id))

    flash(f"Film '{title}' wurde erfolgreich hinzugefügt!", "success")
    return redirect(url_for("get_movies", user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id: int, movie_id: int):
    """
    Updates the title of a movie.
    """
    raw_title = request.form.get("title") or ""
    new_title = " ".join(raw_title.split())

    if not new_title:
        flash("Bitte gib einen Filmtitel ein.", "error")
        return redirect(url_for("get_movies", user_id=user_id))

    dm.update_movie(movie_id, new_title)
    flash("Titel wurde aktualisiert.", "success")
    return redirect(url_for("get_movies", user_id=user_id))

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id: int, movie_id: int):
    """
    Deletes a movie belonging to a user.
    """
    dm.delete_movie(movie_id)
    flash("Film wurde gelöscht.", "success")
    return redirect(url_for("get_movies", user_id=user_id))

@app.errorhandler(404)
def page_not_found(error):
    """
    Benutzerdefinierte 404-Seite.
    Erwartet die Datei templates/404.html.
    Wird angezeigt, wenn eine Seite oder Ressource nicht gefunden wird.
    """
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Benutzerdefinierte 500-Seite.
    Erwartet die Datei templates/500.html.
    Dieser Fehler tritt auf, wenn ein unerwarteter Serverfehler auftritt.
    Der Fehler wird zusätzlich im Log gespeichert, um die Fehlersuche zu erleichtern.
    """
    app.logger.exception("Serverfehler: %s", error)
    return render_template("500.html"), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
