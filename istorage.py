from abc import ABC, abstractmethod


class IStorage(ABC):
    """Parent class for all the different storage
    types to inherit from
    """
    @abstractmethod
    def list_movies(self):
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.

        For example, the function may return:
        {
          "Titanic": {
            "rating": 9,
            "year": 1999
          },
          "..." {
            ...
          },
        }
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster_url, imdbID):
        """
        Adds a movie to the movie database.
        Loads the information from a file, adds the movie,
        and saves it. The function doesn't need to validate the input.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Deletes a movie from the movie database.
        Loads the information from a file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        pass

    @abstractmethod
    def update_movie(self, title, notes):
        """
        Updates a movie from the movie database.
        Loads the information from a file, updates the movie,
        and saves it. The function doesn't need to validate the input.
        """
        pass
