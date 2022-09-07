person_roles_find = {
    'actor': '{ "query": { "match_phrase": { "actors_names": "%s" } } }',
    'writer': '{ "query": { "match_phrase": { "writers_names": "%s" } } }',
    'director': '{ "query": { "match_phrase": { "directors_names": "%s" } } }'
}
