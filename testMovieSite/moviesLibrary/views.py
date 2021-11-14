from django.db.models import Count, Avg, F
from django.http import HttpRequest
from django.shortcuts import render
from rest_framework import viewsets, routers
from rest_framework.response import Response

from .models import Movie, Actor
from .serializers import GenreSerializer, ActorSerializer, DirectorSerializer


def index(request):
    return render(request, "moviesLibrary/index.html")


class GenreViewSet(viewsets.GenericViewSet):

    queryset = Movie.objects
    serializer_class = GenreSerializer

    def list(self, request: HttpRequest) -> Response:

        # Кол-во фильмов жанра, Средняя оценка фильмов жанра
        self.queryset = self.queryset.values("genre").annotate(
            movie_count=Count("genre"), avg_rating=Avg("imdb_rating")
        )

        paginated_movies = self.paginate_queryset(self.queryset)
        serializer = self.serializer_class(paginated_movies, many=True)
        return Response(self.paginator.get_paginated_response(serializer.data).data)


class ActorViewSet(viewsets.GenericViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def list(self, request: HttpRequest) -> Response:
        actor = self.queryset.values("movies_for_actors__title").first()

        # была попытка перенести логику ниже с сериалайзер, но тогда получалось по обращению в БД на каждого актера,
        # если оставить как есть - только 2 обращения на всех (жадность во мне победила возможную красоту этого метода)
        actors_qs = self.queryset.values(actor_name=F("name")).annotate(
            movies_count=Count("movies_for_actors")
        )

        # получаем, какие актеры попадут в нашу выборку, в результате пагинации запроса
        actors = self.paginate_queryset(actors_qs)

        avg_genre_rating_for_movies_of_actors = tuple(
            self.queryset.values("name", genre=F("movies_for_actors__genre"))
            .annotate(avg=Avg("movies_for_actors__imdb_rating"))
            .filter(name__in=[actor["actor_name"] for actor in actors])
        )
        by_actor = {}
        for row in avg_genre_rating_for_movies_of_actors:
            name, genre, avg = row.values()
            by_actor.setdefault(name, []).append({"genre": genre, "avg": avg})

        for actor in actors:
            actor_name, _ = actor.values()
            max_avg = max([x["avg"] for x in by_actor[actor_name]])
            actor["best_genre"] = [
                x["genre"] for x in by_actor[actor_name] if x["avg"] == max_avg
            ][0]

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

        serializer = self.serializer_class(actors, many=True)
        return Response(self.paginator.get_paginated_response(serializer.data).data)


class DirectorViewSet(viewsets.GenericViewSet):

    queryset = Movie.objects.all()
    serializer_class = DirectorSerializer

    def list(self, request: HttpRequest) -> Response:
        # получаем, какие режисеры попадут в нашу выборку, в результате пагинации запроса
        needed_directors = self.paginate_queryset(
            self.queryset.values_list("director", flat=True).distinct()
        )

        # запрос по всем режиссерам, актерам, снимавшихся в их фильмах
        directors_with_actor_and_actor_movie_count = (
            self.queryset.filter(director__in=needed_directors)
            .values(director_name=F("director"), name=F("actors__name"))
            .annotate(movie_count=Count("title", distinct=True))
            .order_by("director", "-movie_count")
        )  # .filter(director__in=[needed_directors])

        actor_and_movie_count_by_director = {}
        for row in directors_with_actor_and_actor_movie_count:
            actor_and_movie_count_by_director.setdefault(
                row["director_name"], {}
            ).setdefault("favourite_actors", []).append(
                {"name": row["name"], "movie_count": row["movie_count"]}
            )

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
                    "favourite_actors": data["favourite_actors"][:3],
                    "best_movies": directors_films,
                }
            )
        serializer = self.serializer_class(result, many=True)

        return Response(self.paginator.get_paginated_response(serializer.data).data)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"^genres", GenreViewSet)
router.register(r"^actors", ActorViewSet)
router.register(r"^directors", DirectorViewSet)
