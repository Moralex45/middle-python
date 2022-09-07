CHECK_TABLES_DATA = '''SELECT EXISTS(
    SELECT 1 FROM {schema}.film_work
             UNION ALL
             SELECT 1 FROM {schema}.genre
                      UNION ALL
                      SELECT 1 FROM {schema}.person
                               UNION ALL
                               SELECT 1 FROM {schema}.genre_film_work
                                        UNION ALL
                                        SELECT 1 FROM {schema}.person_film_work)'''

INSERT_GENRE = '''INSERT INTO {schema}.genre (id, name, description, created, modified) VALUES (%s, %s, %s, %s, %s)'''

INSERT_PERSON = '''INSERT INTO {schema}.person (id, full_name, created, modified) VALUES (%s, %s, %s, %s)'''

INSERT_FILM_WORK = '''INSERT INTO {schema}.film_work (id, title, description, creation_date, rating, type, created, modified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''

INSERT_GENRE_FILMWORK = '''INSERT INTO {schema}.genre_film_work (id, genre_id, film_work_id, created) VALUES (%s, %s, %s, %s)'''

INSERT_PERSON_FILMWORK = '''INSERT INTO {schema}.person_film_work (id, person_id, film_work_id, role, created) VALUES (%s, %s, %s, %s, %s)'''
