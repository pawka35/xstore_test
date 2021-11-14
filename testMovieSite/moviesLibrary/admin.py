from django.contrib import admin
from .models import Actor, Writer, Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'imdb_rating', 'genre', 'description', 'director', )
    readonly_fields = ('writers_names', 'actors_names',)


admin.site.register(Actor)
admin.site.register(Writer)


