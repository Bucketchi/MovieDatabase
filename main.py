from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv
import sys

if sys.argv[1].endswith(".json"):
    storage = StorageJson(sys.argv[1])
elif sys.argv[1].endswith(".csv"):
    storage = StorageCsv(sys.argv[1])

movie_app = MovieApp(storage)
movie_app.run()
