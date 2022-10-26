GET_GENRES_SET = '''SELECT
    g.id,
    g.modified,
    g.name,
    g.description
FROM {schema}.genre g
WHERE g.modified > '{modified}'
ORDER BY g.modified
LIMIT {batch_size}'''
