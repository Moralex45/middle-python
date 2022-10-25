from rest_framework import serializers

from movies.models import FilmWork


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.ListSerializer(child=serializers.CharField(source='genre.name'))
    actors = serializers.ListSerializer(child=serializers.CharField())
    directors = serializers.ListSerializer(child=serializers.CharField())
    writers = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        model = FilmWork
        fields = (
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
            'genres',
            'actors',
            'directors',
            'writers',
        )
