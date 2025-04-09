from flask import Flask
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import requests
from .data_manager_interface import DataManagerInterface
from .models import db, User, Movie


class SQLiteDataManager(DataManagerInterface):
    """
    A SQLite-based data manager that handles database operations for users and movies.
    """

    def __init__(self, db_file_name):
        """
        Initializes the SQLiteDataManager, sets up Flask and SQLAlchemy,
        and creates database tables if they don't exist.

        Args:
            db_file_name (str): The SQLite database file path.
        """
        self.app = Flask(__name__, template_folder="../templates", static_folder="../static")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///../{db_file_name}'
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.app.config['SECRET_KEY'] = '6b809f7762e4a672f4d57d951d87c67bff1991ee9eea687d' # for flash messages

        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def get_all_users(self):
        """
        Retrieves all users from the database.

        Returns:
            list: A list of User objects.
        """
        try:
            with self.app.app_context():
                return db.session.query(User).all()
        except SQLAlchemyError as e:
            return f"Error retrieving users: {e}"

    def get_user_movies(self, user_id):
        """
        Retrieves all movies associated with a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of Movie objects belonging to the user.
        """
        try:
            with self.app.app_context():
                return db.session.query(Movie).filter(Movie.user_id == user_id).all()
        except SQLAlchemyError as e:
            return f"Error retrieving movies for user {user_id}: {e}"

    def add_user(self, name, pin, email):
        try:
            with self.app.app_context():
                new_user = User(name=name, pin=pin, email=email)
                db.session.add(new_user)
                db.session.commit()
                return f"User '{name}' added to the database."
        except IntegrityError as e:
            db.session.rollback()  # Rollback if there's an integrity error
            return f"Error adding user. It seems there might be a duplicate entry: {e}"
        except SQLAlchemyError as e:
            db.session.rollback()
            return f"Error adding user: {e}"

    def add_movie(self, title, rating, year, genre, summary, poster, user_id):
        """
        Adds a new movie to the database.

        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (float): The movie rating (e.g., IMDb rating).
            poster (str): URL or file path of the movie poster.

        Returns:
            str: A confirmation message.
        """
        try:
            with self.app.app_context():
                new_movie = Movie(title=title, year=year, rating=rating, genre=genre, summary=summary, poster=poster, user_id=user_id)
                db.session.add(new_movie)
                db.session.commit()
                return f"Added movie '{title}' to the database."
        except IntegrityError as e:
            db.session.rollback()
            return f"Error adding movie. It seems there might be a duplicate movie or missing data: {e}"
        except SQLAlchemyError as e:
            db.session.rollback()
            return f"Error adding movie: {e}"

    def update_movie(self, title, rating, year, genre, summary):
        """
        Updates the rating of an existing movie.

        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating.

        Returns:
            str: A confirmation message.
        """
        try:
            with self.app.app_context():
                movie = db.session.query(Movie).filter(Movie.title == title).first()
                if movie:
                    movie.title = title
                    movie.rating = rating
                    movie.year = year
                    movie.genre = genre
                    movie.summary = summary
                    db.session.commit()
                    return f"Updated movie '{title}' in the database."
                return f"Movie '{title}' not found."
        except SQLAlchemyError as e:
            db.session.rollback()
            return f"Error updating movie: {e}"

    def delete_movie(self, movie_id):
        """
        Deletes a movie from the database.

        Args:
            title (str): The title of the movie to delete.

        Returns:
            str: A confirmation message.
        """
        try:
            with self.app.app_context():
                movie = db.session.query(Movie).filter(Movie.id == movie_id).first()
                if movie:
                    db.session.delete(movie)
                    db.session.commit()
                    return f"Deleted movie from the database."
                return f"Movie not found."
        except SQLAlchemyError as e:
            db.session.rollback()
            return f"Error deleting movie: {e}"

    @staticmethod
    def fetch_movie_data(movie):
        """
        Loads movie details from OMDB.

        :param: movie: string name of movie
        :return: title, rating, year, poster_image_url
        """
        try:
            API_KEY = "9286827"
            search_q = "&t="
            URL = "https://www.omdbapi.com/?apikey=" + API_KEY + search_q

            movie_url = URL + movie
            res = requests.get(movie_url)
            res.raise_for_status()  # Raise an error for bad status codes (4xx, 5xx)
            data = res.json()

            if data.get('Response') == 'False':
                raise ValueError(f"Movie '{movie}' not found in OMDb database.")

            title = data['Title']
            rating = data['imdbRating']
            year = int(data['Year'])
            poster_image_url = data['Poster']
            genre = data['Genre']
            summary = data['Plot']

            return title, rating, year, genre, summary, poster_image_url

        except requests.exceptions.RequestException as e:
            # Catch connection issues, timeout, etc.
            return f"Failed to connect to OMDb API: {e}"
        except ValueError as e:
            return str(e)  # Return the error message from the OMDb API response
        except KeyError as e:
            return f"Missing expected data from OMDb API response: {e}"
        except Exception as e:
            return f"An unexpected error occurred while fetching movie data: {e}"
