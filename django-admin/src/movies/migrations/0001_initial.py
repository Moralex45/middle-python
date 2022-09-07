# Generated by Django 3.2 on 2022-07-04 09:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FilmWork',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(db_index=True, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('creation_date', models.DateField(blank=True, db_index=True, verbose_name='creation_date')),
                ('rating', models.FloatField(blank=True, db_index=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='rating')),
                ('type', models.TextField(blank=True, choices=[('movie', 'movie'), ('tv_show', 'tv_show')], verbose_name='type')),
            ],
            options={
                'verbose_name': 'film_work_verbose_name',
                'verbose_name_plural': 'film_work_verbose_name_plural',
                'db_table': 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'genre_verbose_name',
                'verbose_name_plural': 'genre_verbose_name_plural',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.TextField(verbose_name='full_name')),
            ],
            options={
                'verbose_name': 'person_verbose_name',
                'verbose_name_plural': 'person_verbose_name_plural',
                'db_table': 'content"."person',
            },
        ),
        migrations.CreateModel(
            name='PersonFilmWork',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.TextField(verbose_name='role')),
                ('film_work', models.ForeignKey(db_column='film_work_id', on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork', verbose_name='film_work')),
                ('person', models.ForeignKey(db_column='person_id', on_delete=django.db.models.deletion.CASCADE, to='movies.person', verbose_name='person')),
            ],
            options={
                'verbose_name': 'person_film_work_verbose_name',
                'verbose_name_plural': 'person_film_work_verbose_name_plural',
                'db_table': 'content"."person_film_work',
                'unique_together': {('person', 'film_work', 'role')},
            },
        ),
        migrations.CreateModel(
            name='GenreFilmWork',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('film_work', models.ForeignKey(db_column='film_work_id', on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork', verbose_name='film_work')),
                ('genre', models.ForeignKey(db_column='genre_id', on_delete=django.db.models.deletion.CASCADE, to='movies.genre', verbose_name='genre')),
            ],
            options={
                'verbose_name': 'genre_film_work_verbose_name',
                'verbose_name_plural': 'genre_film_work_verbose_name_plural',
                'db_table': 'content"."genre_film_work',
                'unique_together': {('film_work', 'genre')},
            },
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='movies.GenreFilmWork', to='movies.Genre', verbose_name='genres'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonFilmWork', to='movies.Person', verbose_name='persons'),
        ),
    ]
