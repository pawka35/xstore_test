from rest_framework import serializers

from .models import Genres


class GenreSerializer(serializers.Serializer):
    """Сериализатор данных для GenreViewSet."""

    def to_representation(self, instance: dict) -> dict:
        """Возвращает подготовленные для отображения данные."""
        instance['genre'] = Genres[instance['genre'].upper()].label
        instance['avg_rating'] = round(instance['avg_rating'], 2)
        return instance


class ActorSerializer(serializers.Serializer):
    """Сериализатор данных для ActorViewSet."""

    def to_representation(self, instance: dict) -> dict:
        """Возвращает подготовленные для отображения данные."""
        instance['best_genre'] = Genres[instance['best_genre'].upper()].label
        return instance


class DirectorSerializer(serializers.Serializer):
    """Сериализатор данных для DirectorViewSet."""
    def to_representation(self, instance: dict) -> dict:
        """Возвращает подготовленные для отображения данные."""
        return instance
