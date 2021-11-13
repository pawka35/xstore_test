from django.db import models
from django.db.models.signals import m2m_changed
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
    pass


class Writer(Staff):
    pass


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
    MUSICAL = ("musical", "мюзикл")
    SCIENTIFIC = ("scientific", "научный")
    ADVENTURE = ("adventure", "приключения")
    REALITY = ("reality", "реалити - шоу")
    FAMILY = ("family", "семейный")
    SPORT = ("sport", "спорт")
    HORRORS = ("horrors", "ужасы")
    FANTASTIC = ("fantastic", "фантастика")


class Movie(models.Model):

    title = models.CharField("название", blank=False, max_length=250)
    imdb_rating = models.FloatField("оценка")
    genre = models.CharField(
        "жанр", choices=Genres.choices, default=Genres.UNKNOWN.value, max_length=50
    )
    description = models.TextField("описание")
    writers = models.ManyToManyField(Writer, related_name="movies_for_writer")
    writers_names = models.TextField("имена сценаристов", blank=True)
    director = models.TextField("директор фильма")
    actors = models.ManyToManyField(Actor, related_name="movies_for_actors")
    actors_names = models.TextField("имена актеров", blank=True)

    def __str__(self) -> str:
        return f"{self.title}"


@receiver(m2m_changed, sender=Movie.writers.through)
def writers_changed_receiver(sender, instance, **kwargs):
    instance.writers_names = ", ".join(
        instance.writers.all().values_list("name", flat=True)
    )
    instance.save()


@receiver(m2m_changed, sender=Movie.actors.through)
def actors_changed_receiver(sender, instance, **kwargs):
    instance.actors_names = ", ".join(
        instance.actors.all().values_list("name", flat=True)
    )
    instance.save()
