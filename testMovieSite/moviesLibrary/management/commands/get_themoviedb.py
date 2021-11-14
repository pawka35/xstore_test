import sys
import requests
import json
from django.core.management import BaseCommand

sys.path.append("../../..")
from moviesLibrary.models import Movie, Actor, Writer, Genres


class Command(BaseCommand):
    API_KEY = "f20b92edde64af192e246f74edff9ebd"
    BASE_URL = "https://api.themoviedb.org/3/"
    HEADERS = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmMjBiOTJlZGRlNjRhZjE5MmUyNDZmNzRlZGZmOWViZCIsInN1YiI6I"
        "jU1MjUxYjMxOTI1MTQxNzI3NjAwMTUxYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.PtZ8mcUQXU"
        "gbKIegr2hMUYlWFcriFPaBv9UvNaF5tlQ"
    }

    def handle(self, *args, **options):
        Actor.objects.all().delete()
        Writer.objects.all().delete()
        Movie.objects.all().delete()

        response = requests.get(
            self.BASE_URL + "/genre/movie/list", headers=self.HEADERS
        )
        genres = json.loads(response.text)["genres"]
        genres = {item["id"]: item["name"] for item in genres}

        response = requests.get(
            self.BASE_URL + "/movie/top_rated?language=ru", headers=self.HEADERS
        )
        movies = json.loads(response.text)
        for movie in movies["results"]:
            genre_id = movie["genre_ids"][0]
            genre_name = genres[genre_id].upper()
            try:
                our_genre = Genres[genre_name]
            except KeyError:
                our_genre = Genres.UNKNOWN

            our_movie, is_new_movie = Movie.objects.get_or_create(
                title=movie["title"],
                imdb_rating=movie["vote_average"],
                genre=our_genre.value,
                description=movie["overview"],
            )

            if is_new_movie:
                print(f"Добавили фильм {movie['title']}")
                staffs_response = requests.get(
                    self.BASE_URL + f"movie/{movie['id']}/credits", headers=self.HEADERS
                )
                staffs = json.loads(staffs_response.text)

                for staff in staffs["cast"]:
                    if staff.get("character"):
                        actor, _ = Actor.objects.get_or_create(name=staff["name"])
                        our_movie.actors.add(actor)

                for staff in staffs["crew"]:
                    if staff.get("job") in ["Story", "Screenplay"]:
                        writer, _ = Writer.objects.get_or_create(name=staff["name"])
                        our_movie.writers.add(writer)

                    if staff.get("job") == "Director":
                        our_movie.director = staff["name"]

            our_movie.save()
