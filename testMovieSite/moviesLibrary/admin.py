from django.contrib import admin
from .models import Actor, Writer, Movie


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'imdb_rating', 'genre', 'description', 'director', )


admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor)
admin.site.register(Writer)


