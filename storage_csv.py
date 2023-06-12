from istorage import IStorage
import csv


class StorageCsv(IStorage):
    """
    A class that defines the operations of the program when using the CSV format.
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.

        The function loads the information from the CSV
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
        result_dict = {}

        with open(self.file_path, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read the header row

            for row in csv_reader:
                key = row[0]  # First item in each row as the key
                values = row[1:]  # Rest of the items as values
                result_dict[key] = {header[i+1]: value for i, value in enumerate(values)}
                if "notes" not in result_dict[key]:
                    result_dict[key]["notes"] = ""

        return result_dict

    def add_movie(self, title, year, rating, poster_url, imdbID):
        """
        Adds a movie to the movie database.
        Loads the information from the CSV file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        dict_of_movies = self.list_movies()

        dict_of_movies[title] = {
            "rating": rating,
            "year": year,
            "imdbID": imdbID,
            "notes": ""
        }
        if poster_url != "N/A":
            dict_of_movies[title]["poster_url"] = poster_url

        header = list(dict_of_movies[next(iter(dict_of_movies))].keys())

        with open(self.file_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['title'] + header)  # Write header row

            for key, values in dict_of_movies.items():
                row = [key] + [values[h] for h in header]
                csv_writer.writerow(row)

    def delete_movie(self, title):
        """
        Deletes a movie from the movie database.
        Loads the information from the CSV file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        dict_of_movies = self.list_movies()
        del dict_of_movies[title]

        header = list(dict_of_movies[next(iter(dict_of_movies))].keys())

        with open(self.file_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['title'] + header)  # Write header row

            for key, values in dict_of_movies.items():
                row = [key] + [values[h] for h in header]
                csv_writer.writerow(row)

    def update_movie(self, title, notes):
        """
        Updates a movie from the movie database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.
        """
        dict_of_movies = self.list_movies()
        dict_of_movies[title]["notes"] = notes

        header = list(dict_of_movies[next(iter(dict_of_movies))].keys())

        with open(self.file_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['title'] + header)  # Write header row

            for key, values in dict_of_movies.items():
                row = [key] + [values[h] for h in header]
                csv_writer.writerow(row)
