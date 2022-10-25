GET_PERSONS_SET = '''SELECT
    p.id,
    p.modified,
    p.full_name
FROM {schema}.person p
WHERE p.modified > '{modified}'
ORDER BY p.modified
LIMIT {batch_size}'''
