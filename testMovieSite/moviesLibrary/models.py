from django.db import models


class Staff(models.Model):
    name = models.CharField('имя', blank=False, max_length=150)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """Возвращает строковое представление экземпляра модели."""
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'[{self.pk}]{self.name}'


class Actor(Staff):
    pass


class Writer(Staff):
    pass


class Genres:
    UNKNOWN = 'unknown'
    COMEDY = 'comedy'
    ACTION = 'action'

    GENRES_CHOISE = {
        (UNKNOWN, 'не определен'),
        (COMEDY, 'комедия'),
        (ACTION, 'боевик')
    }


class Movie(models.Model):

    title = models.CharField('название', blank=False, max_length=250)
    imdb_rating = models.FloatField('оценка')
    genre = models.CharField('жанр', choices=Genres.GENRES_CHOISE, default=Genres.UNKNOWN, max_length=50)
    description = models.TextField('описание')
    writers = models.ManyToManyField(Writer, related_name='movies_for_writer')
    writers_names = models.TextField('имена сценаристов', blank=True)
    director = models.TextField('директор фильма')
    actors = models.ManyToManyField(Actor, related_name='movies_for_actors')
    actors_names = models.TextField('имена актеров', blank=True)

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        actors_names = set(self.actors.all().values_list('name', flat=True))
        writers_names = set(self.writers.all().values_list('name', flat=True))

        self.writers_names = ', '.join(writers_names)
        self.actors_names = ', '.join(actors_names)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.title}'
