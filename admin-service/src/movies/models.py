import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models


class CreatedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        abstract = True


class ModifiedMixin(models.Model):
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(ModifiedMixin, CreatedMixin, UUIDMixin):
    name = models.CharField(_('name'), max_length=255, unique=True, db_index=True)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre_verbose_name')
        verbose_name_plural = _('genre_verbose_name_plural')


class FilmWork(ModifiedMixin, CreatedMixin, UUIDMixin):
    class FilmWorkType(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv_show')

    title = models.TextField(_('title'), db_index=True)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation_date'), blank=True, null=True, db_index=True)
    rating = models.FloatField(_('rating'), blank=True, null=True, db_index=True, validators=[MinValueValidator(0),
                                                                                              MaxValueValidator(100)])
    type = models.TextField(_('type'), choices=FilmWorkType.choices, blank=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    genres = models.ManyToManyField('Genre', through='GenreFilmWork', verbose_name=_('genres'))
    persons = models.ManyToManyField('Person', through='PersonFilmWork', verbose_name=_('persons'))

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film_work_verbose_name')
        verbose_name_plural = _('film_work_verbose_name_plural')


class Person(ModifiedMixin, CreatedMixin, UUIDMixin):
    full_name = models.TextField(_('full_name'))

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person_verbose_name')
        verbose_name_plural = _('person_verbose_name_plural')


class GenreFilmWork(CreatedMixin, UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE, db_column='film_work_id',
                                  verbose_name=_('film_work'))
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, db_column='genre_id', verbose_name=_('genre'))

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('genre_film_work_verbose_name')
        verbose_name_plural = _('genre_film_work_verbose_name_plural')

        unique_together = ['film_work', 'genre']


class PersonFilmWork(CreatedMixin, UUIDMixin):
    class FilmWorkRole(models.TextChoices):
        ACTOR = 'actor', _('actor')
        WRITER = 'writer', _('writer')
        DIRECTOR = 'director', _('director')

    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE, db_column='film_work_id',
                                  verbose_name=_('film_work'))
    person = models.ForeignKey('Person', on_delete=models.CASCADE, db_column='person_id', verbose_name=_('person'))
    role = models.TextField(_('role'), choices=FilmWorkRole.choices)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('person_film_work_verbose_name')
        verbose_name_plural = _('person_film_work_verbose_name_plural')

        unique_together = ['person', 'film_work', 'role']
