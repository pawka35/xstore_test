from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import m2m_changed, pre_delete
from django.dispatch import receiver


class Staff(models.Model):

    name = models.CharField("имя", blank=False, max_length=150)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        """Возвращает строковое представление экземпляра модели."""
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"[{self.pk}]{self.name}"


class Actor(Staff):
    class Meta:
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"


class Writer(Staff):
    class Meta:
        verbose_name = "Сценарист"
        verbose_name_plural = "Сценаристы"


class Genres(models.TextChoices):
    UNKNOWN = ("unknown", "не определен")
    ANIME = ("anime", "аниме")
    BIO = ("bio", "биографический")
    ACTION = ("action", "боевик")
    WESTERN = ("western", "вестерн")
    MILITARY = ("military", "военный")
    DETECTIVE = ("detective", "детектив")
    CHILDREN = ("children", "детский")
    DOCUMENTARY = ("documentary", "документальный")
    DRAMA = ("drama", "драма")
    HISTORICAL = ("historical", "исторический")
    COMEDY = ("comedy", "комедия")
    CONCERT = ("concert", "концерт")
    SHORT = ("short", "короткометражный")
    CRIMINAL = ("criminal", "криминал")
    MELODRAMA = ("melodrama", "мелодрама")
    MYSTIC = ("mystic", "мистика")
    MUSIC = ("music", "музыка")
    CARTOON = ("cartoon", "мультфильм")
    ANIMATION = ("animation", "анимационный фильм")
    MUSICAL = ("musical", "мюзикл")
    SCIENTIFIC = ("scientific", "научный")
    ADVENTURE = ("adventure", "приключения")
    REALITY = ("reality", "реалити - шоу")
    FAMILY = ("family", "семейный")
    SPORT = ("sport", "спорт")
    HORRORS = ("horrors", "ужасы")
    FANTASTIC = ("fantastic", "фантастика")


class Movie(models.Model):
    """Модель для фильма."""

    title = models.CharField("название", blank=False, max_length=250)
    imdb_rating = models.FloatField(
        "оценка",
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
    )
    genre = models.CharField(
        "жанр", choices=Genres.choices, default=Genres.UNKNOWN.value, max_length=50
    )
    description = models.TextField("описание")
    writers = models.ManyToManyField(Writer, related_name="movies_for_writer")
    writers_names = models.TextField("имена сценаристов", blank=True)
    director = models.TextField("директор фильма")
    actors = models.ManyToManyField(Actor, related_name="movies_for_actors")
    actors_names = models.TextField("имена актеров", blank=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self) -> str:
        return f"{self.title}"


@receiver(m2m_changed, sender=Movie.writers.through)
def writers_changed_receiver(sender, instance: Movie, **kwargs):
    """Обновляет список имен сценаристов при добавлении к фильму сценариста."""

    instance.writers_names = ", ".join(
        instance.writers.all().values_list("name", flat=True)
    )
    instance.save()


@receiver(m2m_changed, sender=Movie.actors.through)
def actors_changed_receiver(sender, instance: Movie, **kwargs):
    """Обновляет список имен актеров при добавлении к фильму актера."""

    instance.actors_names = ", ".join(
        instance.actors.all().values_list("name", flat=True)
    )
    instance.save()


@receiver(pre_delete, sender=Actor)
def actor_delete_receive(sender: Actor, instance: Actor, **kwargs) -> None:
    """Обновляет список имен актеров при удалении актера."""

    movies_to_update = Movie.objects.filter(actors_names__contains=instance.name)
    for movie in movies_to_update:
        movie.actors_names = exclude_value_from_string(
            movie.actors_names, instance.name
        )
        movie.save()


@receiver(pre_delete, sender=Writer)
def writer_delete_receive(sender: Writer, instance: Writer, **kwargs) -> None:
    """Обновляет список имен сценаристов при удалении сценариста."""

    movies_to_update = Movie.objects.filter(writers_names__contains=instance.name)
    for movie in movies_to_update:
        movie.writers_names = exclude_value_from_string(
            movie.writers_names, instance.name
        )
        movie.save()


def exclude_value_from_string(string: str, excluded_value: str) -> str:
    """Возвращает новую строку с исключенным элементом excluded_value."""

    list_from_string = string.split(", ")
    try:
        list_from_string.remove(excluded_value)
    except ValueError:
        return string
    return ", ".join(list_from_string)
