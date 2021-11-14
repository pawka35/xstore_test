from django.test import TestCase

from .models import Movie, Actor, Writer, Genres


class MoviesTest(TestCase):
    def setUp(self):
        self.actor1 = Actor.objects.create(name="actor1")
        self.actor2 = Actor.objects.create(name="actor2")
        self.writer = Writer.objects.create(name="writer1")

    def test_writers_and_actors_name_add(self) -> None:
        """Проверяет создание записей в полях для имен актеров и сценаристов."""
        movie = Movie(
            title="testMovie",
            imdb_rating=9.0,
            director="director",
            description="some movie",
            genre=Genres.COMEDY.value,
        )
        movie.save()
        movie.actors.add(self.actor1)
        movie.actors.add(self.actor2)
        movie.writers.add(self.writer)

        self.assertEqual(
            f"{self.actor1}, {self.actor2}",
            movie.actors_names,
            "имена актеров добавились неверно",
        )
        self.assertEqual(
            f"{self.writer}", movie.writers_names, "имена сценаристов добавились неверно"
        )
