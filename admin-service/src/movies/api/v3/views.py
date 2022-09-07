from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from rest_framework import viewsets
from .serializers import MovieSerializer

from movies.models import FilmWork, PersonFilmWork


class MoviesApiMixin:
    model = FilmWork

    @classmethod
    def get_queryset(cls):
        return cls.model.objects.prefetch_related('genres', 'persons').all().values() \
            .annotate(genres=ArrayAgg('genres__name', distinct=True)) \
            .annotate(actors=ArrayAgg('persons__full_name',
                                      filter=Q(personfilmwork__role__icontains=PersonFilmWork.FilmWorkRole.ACTOR),
                                      distinct=True)) \
            .annotate(directors=ArrayAgg('persons__full_name',
                                         filter=Q(personfilmwork__role__icontains=PersonFilmWork.FilmWorkRole.DIRECTOR),
                                         distinct=True)) \
            .annotate(writers=ArrayAgg('persons__full_name',
                                       filter=Q(personfilmwork__role__icontains=PersonFilmWork.FilmWorkRole.WRITER),
                                       distinct=True))


class MoviesViewSet(viewsets.ModelViewSet):
    queryset = MoviesApiMixin.get_queryset()
    # model = FilmWork
    serializer_class = MovieSerializer

    # def get_queryset(self):
    #     return self.model.objects.prefetch_related('genres', 'persons').all().values() \
    #         .annotate(genres=ArrayAgg('genres__name', distinct=True)) \
    #         .annotate(actors=ArrayAgg('persons__full_name',
    #                                   filter=Q(personfilmwork__role__icontains=PersonFilmWork.FilmWorkRole.ACTOR),
    #                                   distinct=True)) \
    #         .annotate(directors=ArrayAgg('persons__full_name',
    #                                      filter=Q(personfilmwork__role__icontains=PersonFilmWork.FilmWorkRole.DIRECTOR),
    #                                      distinct=True)) \
    #         .annotate(writers=ArrayAgg('persons__full_name',
    #                                    filter=Q(personfilmwork__role__icontains=PersonFilmWork.FilmWorkRole.WRITER),
    #                                    distinct=True))
