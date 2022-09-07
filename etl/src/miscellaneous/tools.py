import time
import traceback
from functools import wraps
from typing import Generator, Iterator

import psycopg2
from elasticsearch import Elasticsearch, helpers

from core.logger import logger
from models.es_genres import ESGenre
from models.es_movies import ESMovie
from models.es_persons import ESPerson


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, attempts_amount=15):
    """
    Декоратор условно плавного увеличения времени задержки на доступ к ресурсу

    :param start_sleep_time: Начальное время задержки
    :param factor: Степень в функции расчета времени задержки
    :param border_sleep_time: Максимальное возможное время задержки
    :param attempts_amount: Количество попыток перед вбрасыванием исключения
    """
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            attempts_counter: int = 0
            while True:
                try:
                    result = func(*args, **kwargs)
                    return result

                except Exception as e:
                    logger.info(f'Raised exception {e} during {func} func processing. '
                                f'Full stacktrace: {traceback.format_exc()}')
                    attempts_counter += 1
                    if attempts_counter == attempts_amount:
                        raise e

                    sleep_time = start_sleep_time * factor ** attempts_counter \
                        if start_sleep_time * factor ** attempts_counter < border_sleep_time else border_sleep_time
                    time.sleep(sleep_time)

        return inner
    return func_wrapper


@backoff()
def pg_connection_fabric(pg_dsn: str):
    return psycopg2.connect(pg_dsn)


# @backoff()
def bulk_load_to_es(es_client: Elasticsearch, gen_data: Generator[dict, None, None]):
    helpers.bulk(es_client, gen_data)


def extract_gen_pg_data(pg_cursor, query: str) -> Generator[list, None, None]:
    pg_cursor.execute(query=query)
    while (result := pg_cursor.fetchone()) is not None:
        yield result


def transform_movies_pg_data(iterator: Iterator[list]) -> Generator[ESMovie, None, None]:
    for raw_data in iterator:
        directors_names: list[str] = []
        writers_names: list[str] = []
        actors_names: list[str] = []
        actors: list[dict] = []
        writers: list[dict] = []
        directors: list[dict] = []

        for raw_person in raw_data[6]:
            if raw_person['person_role'] == 'director':
                directors_names.append(raw_person['person_name'])
                directors.append({'id': raw_person['person_id'], 'name': raw_person['person_name']})

            elif raw_person['person_role'] == 'actor':
                actors_names.append(raw_person['person_name'])
                actors.append({'id': raw_person['person_id'], 'name': raw_person['person_name']})

            elif raw_person['person_role'] == 'writer':
                writers_names.append(raw_person['person_name'])
                writers.append({'id': raw_person['person_id'], 'name': raw_person['person_name']})

        genres: list[dict] = []

        for raw_genre in raw_data[7]:
            genres.append({'id': raw_genre['genre_id'], 'name': raw_genre['genre_name']})

        es_movie = ESMovie(id=raw_data[0],
                           imdb_rating=raw_data[4],
                           genre=genres,
                           title=raw_data[2],
                           description=raw_data[3],
                           directors_names=directors_names,
                           actors_names=actors_names,
                           writers_names=writers_names,
                           actors=actors,
                           writers=writers,
                           directors=directors)

        yield es_movie


def transform_genres_pg_data(iterator: Iterator[list]) -> Generator[ESGenre, None, None]:
    for raw_data in iterator:
        es_genre = ESGenre(id=raw_data[0], name=raw_data[2])

        yield es_genre


def transform_persons_pg_data(iterator: Iterator[list]) -> Generator[ESPerson, None, None]:
    for raw_data in iterator:
        es_genre = ESPerson(id=raw_data[0], full_name=raw_data[2])

        yield es_genre
