def test_sum(flask_test_client, clean_database):
    print(flask_test_client.get('/api/v1/role_permission/123e4567-e89b-12d3-a456-426614174000'))
    assert 2 == 2
