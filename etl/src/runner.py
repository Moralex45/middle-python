import datetime
import time

from elasticsearch import Elasticsearch

from core.config import Settings
from core.es_index_body import (GENRES_INDEX_BODY, MOVIES_INDEX_BODY,
                                PERSONS_INDEX_BODY)
from core.logger import logger
from miscellaneous import state, storage, tools
from queries import genres, movies, persons


def main():
    configs = Settings()

    etl_state_storage: storage.YMLFileStorage = storage.YMLFileStorage(configs.state_file_path)
    etl_state: state.State = state.State(etl_state_storage)

    es_client: Elasticsearch = Elasticsearch([configs.elasticsearch_connection_url])

    while not es_client.ping():
        time.sleep(configs.main_cycle_sleep_time)

    # ------------------------------------------------------------------------------------------------------------------

    movies_state_keys = [
        'movies_index_modified_filmworks', 'movies_index_modified_genres', 'movies_index_modified_persons'
    ]
    genres_state_keys = ['genres_index_modified_genres']
    persons_state_keys = ['person_index_modified_persons']
    state_key_to_pg_query = {
        'movies_index_modified_filmworks': movies.GET_FILMWORKS_SET_BY_MODIFIED_FILMWORKS,
        'movies_index_modified_genres': movies.GET_FILMWORKS_SET_BY_MODIFIED_GENRES,
        'movies_index_modified_persons': movies.GET_FILMWORKS_SET_BY_MODIFIED_PERSONS,

        'genres_index_modified_genres': genres.GET_GENRES_SET,

        'person_index_modified_persons': persons.GET_PERSONS_SET
    }

    # ------------------------------------------------------------------------------------------------------------------

    all_state_keys = [*movies_state_keys, *genres_state_keys, *persons_state_keys]

    for state_key in all_state_keys:
        if etl_state.get_state(state_key) is None:
            earliest_modified_data = datetime.datetime.min

            etl_state.set_state(state_key, earliest_modified_data)
            logger.info(f'genres {state_key} state key updated to: {earliest_modified_data}')

    # ------------------------------------------------------------------------------------------------------------------

    es_index_name_to_es_index_body = {
        configs.movies_elastic_search_index_name: MOVIES_INDEX_BODY,
        configs.genres_elastic_search_index_name: GENRES_INDEX_BODY,
        configs.persons_elastic_search_index_name: PERSONS_INDEX_BODY
    }

    for es_index_name, es_index_body in es_index_name_to_es_index_body.items():
        if not es_client.indices.exists(es_index_name):
            es_client.indices.create(index=es_index_name, body=es_index_body)
            logger.info(f'ES index {es_index_name} created')

    while True:
        try:
            with tools.pg_connection_fabric(configs.pg_dsn).cursor() as cursor:
                for state_key, pg_query in state_key_to_pg_query.items():
                    raw_pg_data_gen = tools.extract_gen_pg_data(
                        pg_cursor=cursor,
                        query=pg_query.format(
                            schema=configs.postgres_schema,
                            modified=str(etl_state.get_state(state_key)),
                            batch_size=configs.load_batch_size)
                    )

                    raw_pg_data = list(raw_pg_data_gen)
                    if len(raw_pg_data):
                        if state_key in movies_state_keys:
                            data = tools.transform_movies_pg_data(iter(raw_pg_data))
                            tools.bulk_load_to_es(
                                es_client,
                                ({'_index': configs.movies_elastic_search_index_name,
                                  '_id': o.dict()['id'],
                                  '_source': o.dict()} for o in data))
                            etl_state.set_state(state_key, raw_pg_data[-1][1])
                            logger.info(f'{state_key} state key updated to: {raw_pg_data[-1][1]}')

                        elif state_key in genres_state_keys:
                            data = tools.transform_genres_pg_data(iter(raw_pg_data))
                            tools.bulk_load_to_es(
                                es_client,
                                ({'_index': configs.genres_elastic_search_index_name,
                                  '_id': o.dict()['id'],
                                  '_source': o.dict()} for o in data))
                            etl_state.set_state(state_key, raw_pg_data[-1][1])
                            logger.info(f'{state_key} state key updated to: {raw_pg_data[-1][1]}')

                        elif state_key in persons_state_keys:
                            data = tools.transform_persons_pg_data(iter(raw_pg_data))
                            tools.bulk_load_to_es(
                                es_client,
                                ({'_index': configs.persons_elastic_search_index_name,
                                  '_id': o.dict()['id'],
                                  '_source': o.dict()} for o in data))
                            etl_state.set_state(state_key, raw_pg_data[-1][1])
                            logger.info(f'{state_key} state key updated to: {raw_pg_data[-1][1]}')

        except Exception as e:
            logger.error(f'Exception raised: {e}')

        time.sleep(configs.main_cycle_sleep_time)


if __name__ == '__main__':
    main()
