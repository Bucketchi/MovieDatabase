import requests
import random

API_KEY = "81cc18ae"
TEMPLATE_HTML = "_static/index_template.html"
SITE_TITLE = "Alex's Favourite Films"
HTML_FILE_NAME = "_static/index.html"
IMDB_URL = "https://www.imdb.com/title/"


class MovieApp:
    """
    A class that defines all the possible operations of the application. Requires a storage to passed
    as an initializer.
    """
    def __init__(self, storage):
        self._storage = storage

    @staticmethod
    def show_menu():
        """
        Prints the app menu to the terminal and receives input from
        the user for their chosen operations.

        Returns the choice as a string.
        """
        print("""\n********** My Movies Database **********

    Menu:
    0. Quit
    1. List movies
    2. Add movie
    3. Delete movie
    4. Update movie
    5. Stats
    6. Random movie
    7. Search movie
    8. Movies sorted by rating
    9. Generate website""")

        choice = input("\nEnter a choice (0-9): ")

        return choice

    def _command_list_movies(self):
        """
        Prints the list of movies and respective ratings to the terminal.
        """
        movies = self._storage.list_movies()
        num_movies = len(movies)
        print(f"\n{num_movies} movies in total")
        for movie, info in movies.items():
            print(f"{movie} ({info['year']}): {info['rating']} ")

    def _command_add_movie(self):
        """
        Receives a name as an input from the user and queries the OMDB API.
        Adds the relevant data from the API to the file.
        """
        new_movie = input("\nEnter movie name: ")
        try:
            res = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t={new_movie}")
        except Exception:
            print("Failed to connect to Movie API")
            return
        movie_info = res.json()
        if movie_info["Response"] == "True":
            try:
                self._storage.add_movie(movie_info["Title"], movie_info["Year"], float(movie_info["imdbRating"]),
                                        movie_info["Poster"], movie_info["imdbID"])
            except ValueError:
                print("Unexpected value in API, could not add movie")
        else:
            print(movie_info["Error"])

    def _command_delete_movie(self):
        """
        Receives a name as an input from the user and deletes the respective movie from the file.
        """
        while True:  # Runs until valid movie title is entered
            movie_name = input("\nEnter a movie you want to delete: ")

            movies = self._storage.list_movies()
            if movie_name in movies:
                self._storage.delete_movie(movie_name)
                break

            print("\nError: Movie not in list!")

    def _command_update_movie(self):
        """
        Requests a movie name from the user to add a note to said movie in the storage file.
        """
        while True:  # Runs until valid movie title is entered
            movie_name = input("\nEnter a movie you want to update: ")
            movies = self._storage.list_movies()
            if movie_name in movies:
                notes = input("\nEnter a note: ")
                self._storage.update_movie(movie_name, notes)
                break
            print("Movie is not in list!\n")

    def _command_movie_stats(self):
        """
        Processes the ratings from all the movies to then print a variety of stats to the terminal.
        """
        movies = self._storage.list_movies()
        sorted_list_of_ratings = list(movies.items())
        sorted_list_of_ratings.sort(key=lambda x: x[1]["rating"], reverse=True)

        # # Calculates average rating
        avg_rating = sum(float(movie[1]["rating"]) for movie in sorted_list_of_ratings) / len(sorted_list_of_ratings)
        print(f"\nThe average rating is: {round(avg_rating, 2)}")

        # Calculates median
        mid = len(sorted_list_of_ratings) // 2
        median = (float(sorted_list_of_ratings[mid][1]["rating"]) + float(sorted_list_of_ratings[~mid][1]["rating"]))/2
        print(f"The median rating is: {round(median, 2)}")

        # Calculates maximum and minimum rating
        max_rating = float(sorted_list_of_ratings[0][1]["rating"])
        min_rating = float(sorted_list_of_ratings[-1][1]["rating"])

        # Prints all movies with max rating
        print("Best movie(s): ", end="")
        for movie, info in movies.items():
            if float(info["rating"]) == max_rating:
                print(f"{movie} : {info['rating']}", end="   ")
        #
        # Prints all movies with min rating
        print("\nWorst movie(s): ", end="")
        for movie, info in movies.items():
            if float(info["rating"]) == min_rating:
                print(f"{movie} : {info['rating']}", end="   ")

    def _command_random_movie(self):
        """
        Gets a random movie from the file and prints to the terminal along with
        the respective rating.
        """
        movies = self._storage.list_movies()
        random_selection = random.choice(list(movies))
        print(f"\n{random_selection} : {movies[random_selection]['rating']}")

    def _command_search_movie(self):
        """
        Requests a string from the user and prints all the movies that contain that
        string.
        """
        movies = self._storage.list_movies()
        # Gets search term from user
        query = input("\nEnter part of the movie name: ")
        found = False
        # Prints movies that include search term
        for movie in movies:
            if query.lower() in movie.lower():
                print(f"{movie} : {movies[movie]['rating']}")
                found = True
        if not found:
            print("Movie not in list.\n")

    def _command_sort_movies(self):
        """
        Processes the ratings of the movies to print a list from highest to lowest rated.
        """
        movies = self._storage.list_movies()
        # Creates a sorted list of movies sorted by rating
        sorted_list_of_ratings = list(movies.items())
        sorted_list_of_ratings.sort(key=lambda x: x[1]["rating"], reverse=True)

        # Prints all the movies in descending order
        for movie, info in sorted_list_of_ratings:
            print(f"{movie} : {info['rating']}")

    def _generate_website(self):
        """
        Parses all the data from the file to generate an HTML file
        based on a template.
        """
        movies = self._storage.list_movies()
        with open(TEMPLATE_HTML, "r") as template:
            html_data = template.read()
        html_data = html_data.replace("__TEMPLATE_TITLE__", SITE_TITLE)

        data_string = ""
        for movie, info in movies.items():
            data_string += "<li>\n      <div class='movie'>\n"
            if "poster_url" in info:
                data_string += f'    <a href={IMDB_URL + info["imdbID"]}>' \
                               f'<img class="movie-poster", src={info["poster_url"]}'
                if "notes" in info:
                    data_string += f', title="{info["notes"]}"></a>\n'
                else:
                    data_string += "></a>\n"
            data_string += f'    <div class="movie-title">{movie}</div>\n    ' \
                           f'<div class="movie-year">{info["year"]} - {info["rating"]} rating</div>\n'
            data_string += "  </div>\n</li>\n"

        html_data = html_data.replace("__TEMPLATE_MOVIE_GRID__", data_string)

        with open(HTML_FILE_NAME, "w") as html_obj:
            html_obj.write(html_data)
        print("Website was generated successfully.")

    def run(self):
        """
        Runs the application in the desired way, calling the Show Menu function
        indefinitely until the user enters the Quit choice.
        """
        while True:
            # Gets menu selection from user
            choice = self.show_menu()

            # Executes function chosen by user
            if choice == "1":
                self._command_list_movies()
            if choice == "2":
                self._command_add_movie()
            if choice == "3":
                self._command_delete_movie()
            if choice == "4":
                self._command_update_movie()
            if choice == "5":
                self._command_movie_stats()
            if choice == "6":
                self._command_random_movie()
            if choice == "7":
                self._command_search_movie()
            if choice == "8":
                self._command_sort_movies()
            if choice == "9":
                self._generate_website()
            # Exits program
            if choice == "0":
                print("Bye!")
                break
