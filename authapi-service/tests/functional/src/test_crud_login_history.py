from http import HTTPStatus

import pytest

from functional.testdata.database_fake_data import users, user_agents


@pytest.mark.parametrize(
    'user',
    [user for user in users])
def test_successful_user_logout_multiply_devices(flask_test_client,
                                                 clean_database,
                                                 clean_cache,
                                                 generate_users,
                                                 server_settings_instance,
                                                 user):
    for user_agent in user_agents:
        request_body = {
            'username': user['username'],
            'password': user['password'],
            'remember': True
        }
        response = flask_test_client.post('/api/v1/auth/login/',
                                          json=request_body,
                                          environ_base={'HTTP_USER_AGENT': user_agent})

        assert response.status_code == HTTPStatus.OK
        assert response.text == ''

    response = flask_test_client.get('/api/v1/crud/user/login_history')

    assert response.status_code == HTTPStatus.OK
    assert response.is_json

    login_history_before_logout = response.json

    assert user_agents.sort() == [session['user_agent'] for session in login_history_before_logout].sort()

    request_body = {
        'all_devices': True
    }
    response = flask_test_client.post('/api/v1/auth/logout/', json=request_body)

    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    request_body = {
        'username': user['username'],
        'password': user['password'],
        'remember': True
    }
    response = flask_test_client.post('/api/v1/auth/login/',
                                      json=request_body,
                                      environ_base={'HTTP_USER_AGENT': user_agents[0]})

    assert response.status_code == HTTPStatus.OK
    assert response.text == ''

    response = flask_test_client.get('/api/v1/crud/user/login_history')

    assert response.status_code == HTTPStatus.OK
    assert response.is_json

    login_history_after_logout = response.json

    assert len(login_history_before_logout) != login_history_after_logout

    login_history_after_logout = list(filter(lambda o: o['date_end'] is not None, login_history_after_logout))
    assert len(login_history_before_logout) == len(login_history_after_logout)

    for session_before_logout, session_after_logout in zip(
            sorted(login_history_before_logout, key=lambda o: o['user_agent']),
            sorted(login_history_after_logout, key=lambda o: o['user_agent'])):
        assert session_before_logout['user_agent'] == session_after_logout['user_agent']
        assert session_before_logout['date_start'] == session_after_logout['date_start']
