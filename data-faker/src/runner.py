import random
import sys
import time
from datetime import datetime, timedelta

import psycopg2
from faker import Faker
from psycopg2.extras import execute_batch

from config import Settings
import queries
from logger import logger


def main():
    settings = Settings()
    fake: Faker = Faker()
    now = datetime.utcnow()

    with psycopg2.connect(settings.postgres_dsn) as conn, conn.cursor() as cursor:
        while True:
            try:
                cursor.execute(query=queries.CHECK_TABLES_DATA.format(schema=settings.POSTGRES_SCHEMA))

            except psycopg2.errors.UndefinedTable:
                conn.commit()
                time.sleep(5)
                logger.info('Unable to establish connection with postgres. Waiting for tables creation')
                continue

            if cursor.fetchone()[0]:
                logger.info('Found tables filled with data. Data faking not permitted')
                sys.exit(0)

            else:
                break

        earliest_modified_data = datetime.min
        genres = []

        while settings.GENRES_AMOUNT > 0:
            generate_amount = settings.GENRES_AMOUNT \
                if settings.GENRES_AMOUNT < settings.LOAD_BATCH_SIZE \
                else settings.LOAD_BATCH_SIZE
            query = queries.INSERT_GENRE.format(schema=settings.POSTGRES_SCHEMA)
            data = [(fake.uuid4(), fake.company() + str(random.randint(0, 100)), fake.catch_phrase(), now,
                     earliest_modified_data := earliest_modified_data + timedelta(seconds=1))
                    for _ in range(generate_amount)]
            genres.extend(data)
            execute_batch(cursor, query, data)
            conn.commit()

            logger.info(f'{generate_amount} rows of fake genres data inserted successfully')

            settings.GENRES_AMOUNT -= generate_amount

        # --------------------------------------------------------------------------------------------------------------

        earliest_modified_data = datetime.min
        persons = []

        while settings.PERSONS_AMOUNT > 0:
            generate_amount = settings.PERSONS_AMOUNT \
                if settings.PERSONS_AMOUNT < settings.LOAD_BATCH_SIZE \
                else settings.LOAD_BATCH_SIZE
            query = queries.INSERT_PERSON.format(schema=settings.POSTGRES_SCHEMA)
            data = [(fake.uuid4(), fake.name(), now,
                     earliest_modified_data := earliest_modified_data + timedelta(seconds=1))
                    for _ in range(generate_amount)]
            persons.extend(data)
            execute_batch(cursor, query, data)
            conn.commit()

            logger.info(f'{generate_amount} rows of fake persons data inserted successfully')

            settings.PERSONS_AMOUNT -= generate_amount

        # --------------------------------------------------------------------------------------------------------------

        earliest_modified_data = datetime.min
        film_work_type_to_setting_value = {'movie': settings.FILMWORKS_MOVIES_AMOUNT,
                                           'tv_show': settings.FILMWORKS_TV_SHOWS_AMOUNT}

        for film_work_type, setting_value in film_work_type_to_setting_value.items():
            while setting_value > 0:
                generate_amount = setting_value \
                    if setting_value < settings.LOAD_BATCH_SIZE \
                    else settings.LOAD_BATCH_SIZE
                temp_filmworks = [
                    {'id': fake.uuid4(),
                     'title': fake.name(),
                     'description': fake.text(),
                     'creation_date': fake.past_date(),
                     'rating': round(random.uniform(0.0, 100.0), 1),
                     'type': film_work_type}
                    for _ in range(generate_amount)]

                query = queries.INSERT_FILM_WORK.format(schema=settings.POSTGRES_SCHEMA)
                data = [
                    (film_work['id'],
                     film_work['title'],
                     film_work['description'],
                     film_work['creation_date'],
                     film_work['rating'],
                     film_work['type'],
                     now,
                     earliest_modified_data := earliest_modified_data + timedelta(seconds=1))
                    for film_work in temp_filmworks]
                execute_batch(cursor, query, data)
                conn.commit()

                logger.info(
                    f'{generate_amount} rows of fake film works type {film_work_type} data inserted successfully')

                setting_value -= generate_amount

                # ------------------------------------------------------------------------------------------------------

                film_works_to_genres = [
                    {film_work['id']: {random.choice(genres)[0] for _ in range(random.randint(
                        settings.GENRES_TO_FILMWORK_MIN_AMOUNT, settings.GENRES_TO_FILMWORK_MAX_AMOUNT))}}
                    for film_work in temp_filmworks]

                data = [
                    (fake.uuid4(), genre_id, film_work_id, now)
                    for film_work_to_genres in film_works_to_genres
                    for film_work_id, genres_ids in film_work_to_genres.items()
                    for genre_id in genres_ids]

                query = queries.INSERT_GENRE_FILMWORK.format(schema=settings.POSTGRES_SCHEMA)
                execute_batch(cursor, query, data)
                conn.commit()

                logger.info(
                    f'{len(data)} rows of fake genre film works type {film_work_type} data inserted successfully')

                # ------------------------------------------------------------------------------------------------------

                person_type_to_amount = {
                    'director': random.randint(settings.DIRECTORS_TO_FILMWORKS_MIN_AMOUNT,
                                               settings.DIRECTORS_TO_FILMWORKS_MAX_AMOUNT),
                    'actor': random.randint(settings.ACTORS_TO_FILMWORKS_MIN_AMOUNT,
                                            settings.ACTORS_TO_FILMWORKS_MAX_AMOUNT),
                    'writer': random.randint(settings.WRITERS_TO_FILMWORKS_MIN_AMOUNT,
                                             settings.WRITERS_TO_FILMWORKS_MAX_AMOUNT)}

                for person_type, amount in person_type_to_amount.items():
                    film_works_to_persons = [
                        {film_work['id']: {random.choice(persons)[0] for _ in range(amount)}}
                        for film_work in temp_filmworks]

                    data = [
                        (fake.uuid4(), person_id, film_work_id, person_type, now)
                        for film_work_to_persons in film_works_to_persons
                        for film_work_id, persons_ids in film_work_to_persons.items()
                        for person_id in persons_ids]

                    query = queries.INSERT_PERSON_FILMWORK.format(schema=settings.POSTGRES_SCHEMA)
                    execute_batch(cursor, query, data)
                    conn.commit()

                    logger.info(
                        f'{len(data)} rows of fake person ({person_type}) film works type {film_work_type} data inserted successfully')


if __name__ == '__main__':
    main()
