from django.db.models import Count, Avg, F
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from rest_framework import viewsets, routers
from rest_framework.response import Response

from .models import Movie, Actor


def index(request):
    context = {}
    return render(request, 'moviesLibrary/index.html', context)


class GenreViewSet(viewsets.ViewSet):

    queryset = Movie.objects

    def list(self, request: HttpRequest) -> Response:
        # Кол-во фильмов этого жанра, Средняя оценка фильмов данного жанра
        result = self.queryset.values("genre").annotate(
            movie_count=Count("genre"), avg_rating=Avg("imdb_rating")
        )

        return Response(result)


class ActorViewSet(viewsets.ViewSet):
    queryset = Actor.objects

    def list(self, request: HttpRequest) -> Response:
        actors = list(
            self.queryset.values(actor_name=F("name")).annotate(
                movies_count=Count("movies_for_actors")
            )
        )

        avg_genre_rating_for_movies_of_actors = tuple(
            self.queryset.values("name", genre=F("movies_for_actors__genre")).annotate(
                avg=Avg("movies_for_actors__imdb_rating")
            )
        )

        by_actor = {}
        for row in avg_genre_rating_for_movies_of_actors:
            name, genre, avg = row.values()
            by_actor.setdefault(name, []).append({"genre": genre, "avg": avg})

        for actor in actors:
            actor_name, _ = actor.values()
            max_avg = max([genres["avg"] for genres in by_actor[actor_name]])
            actor["best_genre"] = max_avg

        # еще был вариант реализации через queryset, но лишние обращения к БД в общем случае - не к чему
        # реализацию приведу для примера
        # for actor in actors:
        #   best_genre_rating = (
        #       genre_rating_by_actor_and_genre.filter(name=actor["actor_name"])
        #       .values_list("avg")
        #       .aggregate(max=Max("avg"))
        #   )
        #
        #   best_genre_name = (
        #     genre_rating_by_actor_and_genre.filter(
        #         name=actor["actor_name"], avg=best_genre_rating["max"]
        #     )
        #     .values_list("movies_for_actors__genre", flat=True)
        #     .first()
        #   )
        #   actor["best_genre"] = best_genre_name

        return Response(actors)


class DirectorViewSet(viewsets.ViewSet):

    queryset = Movie.objects

    def list(self, request: HttpRequest) -> Response:

        directors_with_actor_and_actor_movie_count = tuple(
            self.queryset.values(director_name=F("director"), name=F("actors__name"))
            .annotate(movie_count=Count("title", distinct=True))
            .order_by("director", "-movie_count")
        )
        actor_and_movie_count_by_director = {}
        # так делать не рекомендуется, т.к. создастся генератор, который нам в дальнейшем не нужен, сделано в целях
        # демонстрации использования List Comprehension
        [
            actor_and_movie_count_by_director.setdefault(x["director_name"], {})
            .setdefault("favourite_actors", [])
            .append({"name": x["name"], "movie_count": x["movie_count"]})
            for x in directors_with_actor_and_actor_movie_count
        ]

        result = []
        for director_name, data in actor_and_movie_count_by_director.items():
            directors_films = list(
                self.queryset.values_list("title", flat=True)
                .filter(director=director_name)
                .order_by("-imdb_rating")[:3]
            )
            actor_and_movie_count_by_director[director_name][
                "director_name"
            ] = director_name
            actor_and_movie_count_by_director[director_name][
                "best_movies"
            ] = directors_films
            result.append(
                {
                    "director_name": director_name,
                    "favourite_actors": data["favourite_actors"],
                    "best_movies": directors_films,
                }
            )
        return Response(result)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"^genres", GenreViewSet)
router.register(r"^actors", ActorViewSet)
router.register(r"^directors", DirectorViewSet)
