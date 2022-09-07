from collections import OrderedDict

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import MovieSerializer

from movies.models import FilmWork, PersonFilmWork


class FooPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.page.next_page_number()),
            ('prev', self.page.previous_page_number()),
            ('total_pages', self.page.paginator.num_pages),
            ('results', data),
        ]))


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


class MoviesListApi(ListAPIView):
    queryset = MoviesApiMixin.get_queryset()
    serializer_class = MovieSerializer
    pagination_class = FooPagination


class MoviesDetailApi(RetrieveAPIView):
    queryset = MoviesApiMixin.get_queryset()
    serializer_class = MovieSerializer
