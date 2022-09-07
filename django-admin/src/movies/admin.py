from django.contrib import admin
from .models import Genre, FilmWork, Person, GenreFilmWork, PersonFilmWork
from .forms import PersonFilmWorkForm


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    form = PersonFilmWorkForm


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline,)

    list_display = ('title', 'type', 'creation_date', 'rating', 'created', 'modified',)
    list_filter = ('type', 'genres',)
    search_fields = ('title', 'description', 'id',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass
