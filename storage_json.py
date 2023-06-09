from istorage import IStorage
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.

        The function loads the information from the JSON
        file and returns the data.

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
        with open(self.file_path, "r") as file_obj:
            dict_of_movies = json.load(file_obj)
            return dict_of_movies

    def add_movie(self, title, year, rating, poster_url, imdbID):

        """
        Adds a movie to the movie database.
        Loads the information from the JSON file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        dict_of_movies = self.list_movies()

        dict_of_movies[title] = {
            "rating": rating,
            "year": year,
            "imdbID": imdbID
        }
        if poster_url != "N/A":
            dict_of_movies[title]["poster_url"] = poster_url

        json_string = json.dumps(dict_of_movies)

        with open(self.file_path, "w") as file_obj:
            file_obj.write(json_string)

    def delete_movie(self, title):
        """
            Deletes a movie from the movie database.
            Loads the information from the JSON file, deletes the movie,
            and saves it. The function doesn't need to validate the input.
            """
        dict_of_movies = self.list_movies()
        del dict_of_movies[title]
        json_string = json.dumps(dict_of_movies)
        with open(self.file_path, "w") as file_obj:
            file_obj.write(json_string)

    def update_movie(self, title, notes):
        """
        Updates a movie from the movie database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.
        """
        dict_of_movies = self.list_movies()
        dict_of_movies[title]["notes"] = notes
        json_string = json.dumps(dict_of_movies)
        with open(self.file_path, "w") as file_obj:
            file_obj.write(json_string)
