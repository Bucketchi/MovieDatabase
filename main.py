from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv
import sys


def main():
    """
    Main function for the application.
    """
    try:
        if sys.argv[1].endswith(".json"):
            storage = StorageJson(sys.argv[1])
        elif sys.argv[1].endswith(".csv"):
            storage = StorageCsv(sys.argv[1])
    except IndexError:
        storage = StorageJson("data.json")

    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
