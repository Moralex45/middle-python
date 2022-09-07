from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork, PersonFilmWork


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        return FilmWork.objects.prefetch_related('genres', 'persons').all().values() \
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

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        movie_instance = kwargs['object']

        del movie_instance['created']
        del movie_instance['modified']
        del movie_instance['file_path']

        return movie_instance


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        required_page_number = self.request.GET.get('page', None)

        try:
            required_page_number = int(required_page_number) if required_page_number != 'last' else 20

        except Exception:
            required_page_number = 1

        page_data = paginator.page(required_page_number)
        movie_list = list(page_data.object_list.values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
            'genres',
            'actors',
            'writers',
            'directors'
        ))

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev':   page.previous_page_number() if page.has_previous() else None,
            'next':   page.next_page_number() if page.has_next() else None,
            'results': movie_list
        }

        return context
