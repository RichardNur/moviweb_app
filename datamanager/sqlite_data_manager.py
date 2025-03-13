from flask import Flask
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
        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///../{db_file_name}'
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        with self.app.app_context():
            db.__init__(self.app)
            db.create_all()  # Ensure tables are created

    def get_all_users(self):
        """
        Retrieves all users from the database.

        Returns:
            list: A list of User objects.
        """
        with self.app.app_context():
            return db.session.query(User).all()

    def get_user_movies(self, user_id):
        """
        Retrieves all movies associated with a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of Movie objects belonging to the user.
        """
        with self.app.app_context():
            return db.session.query(Movie).filter(Movie.user_id == user_id).all()

    def add_user(self, name, email):

        with self.app.app_context():
            new_user = User(name=name, email=email)
            db.session.add(new_user)
            db.session.commit()
            return f"User '{name}' added to the database."

    def add_movie(self, title, year, rating, poster):
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
        with self.app.app_context():
            new_movie = Movie(title=title, year=year, rating=rating, poster=poster)
            db.session.add(new_movie)
            db.session.commit()
            return f"Added movie '{title}' to the database."

    def update_movie(self, title, rating):
        """
        Updates the rating of an existing movie.

        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating.

        Returns:
            str: A confirmation message.
        """
        with self.app.app_context():
            movie = db.session.query(Movie).filter(Movie.title == title).first()
            if movie:
                movie.rating = rating
                db.session.commit()
                return f"Updated movie '{title}' in the database."
            return f"Movie '{title}' not found."

    def delete_movie(self, title):
        """
        Deletes a movie from the database.

        Args:
            title (str): The title of the movie to delete.

        Returns:
            str: A confirmation message.
        """
        with self.app.app_context():
            movie = db.session.query(Movie).filter(Movie.title == title).first()
            if movie:
                db.session.delete(movie)
                db.session.commit()
                return f"Deleted movie '{title}' from the database."
            return f"Movie '{title}' not found."