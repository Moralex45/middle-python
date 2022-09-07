def transform_movies_test_data(test_data: dict) -> dict:

    test_data = test_data.copy()
    test_data['uuid'] = test_data['id']
    test_data['genre'] = [
        {'uuid': genre['id'], 'name': genre['name']} for genre in test_data['genre']
        ]
    test_data['directors'] = [
        {'uuid': director['id'], 'full_name': director['name']} for director in test_data['directors']
        ]
    test_data['actors'] = [
        {'uuid': actor['id'], 'full_name': actor['name']} for actor in test_data['actors']
        ]
    test_data['writers'] = [
        {'uuid': writer['id'], 'full_name': writer['name']} for writer in test_data['writers']
        ]

    del (test_data['id'])
    del (test_data['actors_names'])
    del (test_data['writers_names'])

    return test_data


def transform_movies_list_test_data(test_data: list) -> list:
    out_test_data = [{'uuid': film['id'], 'title': film['title'], 'imdb_rating': film['imdb_rating']}
                     for film in test_data]
    return out_test_data


def transform_genre_test_data(test_data: dict) -> dict:
    test_data = test_data.copy()
    test_data['uuid'] = test_data['id']
    del (test_data['id'])
    return test_data


def transform_genre_list_test_data(test_data: list) -> list:
    out_test_data = [{'uuid': genre['id'], 'name':genre['name']}
                     for genre in test_data]
    return out_test_data


def transform_person_test_data(test_data: dict) -> dict:
    test_data = test_data.copy()
    test_data['uuid'] = test_data['id']
    del (test_data['id'])
    return test_data


def transform_person_list_test_data(test_data: list) -> list:
    out_test_data = [{'uuid': person['id'], 'name':person['name']}
                     for person in test_data]
    return out_test_data


def prepare_person_film_data(person_data: dict, test_movies: list[dict]) -> list[dict]:
    out = []
    for movie in test_movies:
        if person_data in movie['actors'] or person_data in movie['writers'] or person_data in movie['directors']:
            out.append({'uuid': movie['id'], 'imdb_rating': movie['imdb_rating'], 'title': movie['title']})
    return out
