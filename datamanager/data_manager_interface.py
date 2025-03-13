from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    """
    An abstract base class that defines the interface for data management operations.
    """

    @abstractmethod
    def get_all_users(self):
        """
        Retrieves all users from the database.

        Returns:
            list: A list of user objects.
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Retrieves all movies associated with a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of movie objects belonging to the user.
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        Adds a movie to the database.

        Args:
            title (str): The title of the movie.
            year (int): The release year of the movie.
            rating (float): The movie rating.
            poster (str): The URL or path to the movie poster.

        Returns:
            str: A confirmation message.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Deletes a movie from the database.

        Args:
            title (str): The title of the movie to delete.

        Returns:
            str: A confirmation message.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Updates the rating of a movie.

        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating.

        Returns:
            str: A confirmation message.
        """
        pass