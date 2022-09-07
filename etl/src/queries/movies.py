GET_FILMWORKS_SET_BY_MODIFIED_PERSONS = '''SELECT
    fw.id,
    max(p.modified),
    fw.title,
    fw.description,
    fw.rating,
    fw.type,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'person_role', pfw.role,
                'person_id', p.id,
                'person_name', p.full_name
                )
            ) FILTER (WHERE p.id is not null),
        '[]'
        ) as persons,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'genre_id', g.id,
                'genre_name', g.name
                )
            ) FILTER (WHERE g.id is not null),
        '[]'
        ) as genres
FROM {schema}.film_work fw
    LEFT JOIN {schema}.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN {schema}.person p ON p.id = pfw.person_id
    LEFT JOIN {schema}.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN {schema}.genre g ON g.id = gfw.genre_id
WHERE fw.id IN (SELECT DISTINCT fw.id
                FROM {schema}.film_work fw
                    LEFT JOIN {schema}.person_film_work pfw ON pfw.film_work_id = fw.id
                WHERE pfw.person_id IN (SELECT id
                                        FROM {schema}.person p
                                        WHERE p.modified > '{modified}'
                ))
GROUP BY fw.id
HAVING max(p.modified) > '{modified}'
ORDER BY max(p.modified)
LIMIT {batch_size}'''

GET_FILMWORKS_SET_BY_MODIFIED_GENRES = '''SELECT
    fw.id,
    max(g.modified),
    fw.title,
    fw.description,
    fw.rating,
    fw.type,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'person_role', pfw.role,
                'person_id', p.id,
                'person_name', p.full_name
                )
            ) FILTER (WHERE p.id is not null),
        '[]'
        ) as persons,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'genre_id', g.id,
                'genre_name', g.name
                )
            ) FILTER (WHERE g.id is not null),
        '[]'
        ) as genres
FROM {schema}.film_work fw
    LEFT JOIN {schema}.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN {schema}.person p ON p.id = pfw.person_id
    LEFT JOIN {schema}.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN {schema}.genre g ON g.id = gfw.genre_id
WHERE fw.id IN (SELECT DISTINCT fw.id
                FROM {schema}.film_work fw
                    LEFT JOIN {schema}.genre_film_work gfw ON gfw.film_work_id = fw.id
                WHERE gfw.genre_id IN (SELECT id
                                       FROM {schema}.genre
                                       WHERE modified > '{modified}'
                ))
GROUP BY fw.id
HAVING max(g.modified) > '{modified}'
ORDER BY max(g.modified)
LIMIT {batch_size}'''

GET_FILMWORKS_SET_BY_MODIFIED_FILMWORKS = '''SELECT
    fw.id,
    fw.modified,
    fw.title,
    fw.description,
    fw.rating,
    fw.type,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'person_role', pfw.role,
                'person_id', p.id,
                'person_name', p.full_name
                )
            ) FILTER (WHERE p.id is not null),
        '[]'
        ) as persons,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'genre_id', g.id,
                'genre_name', g.name
                )
            ) FILTER (WHERE g.id is not null),
        '[]'
        ) as genres
FROM {schema}.film_work fw
    LEFT JOIN {schema}.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN {schema}.person p ON p.id = pfw.person_id
    LEFT JOIN {schema}.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN {schema}.genre g ON g.id = gfw.genre_id
WHERE fw.modified > '{modified}'
GROUP BY fw.id
ORDER BY fw.modified
LIMIT {batch_size}'''
