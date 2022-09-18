roles = [
    {
        'id': '53877241-56a9-4c0e-92fb-57dfcfd63f8e',
        'code': 1,
        'description': 'content-manager'
    },
    {
        'id': 'de7e3e01-16b4-452d-83c8-837ea976c564',
        'code': 2,
        'description': 'manager-content-manager'
    },
    {
        'id': 'e42c19f9-41a8-4dcd-865d-c9c85d20ad85',
        'code': 3,
        'description': 'manager-manager-content-manager'
    }
]

permissions = [
    {
        'id': 'e0de2cb6-db6b-4e03-8426-e74eac73801a',
        'code': 1,
    },
    {
        'id': 'd48f6bb1-c060-49da-a9b0-d04af161b7ed',
        'code': 2,
    },
    {
        'id': 'aafebc0a-6396-4f9d-bfca-51089df12319',
        'code': 3,
    },
    {
        'id': '175d8060-d108-4898-af38-ffc4000027fc',
        'code': 4,
    },
    {
        'id': '7a11716c-819d-4929-866d-d5093fd253a2',
        'code': 5,
    }
]

roles_permissions = [
    {
        'id': '809378b2-c567-4c83-a4c8-120768787abf',
        'role_id': roles[0]['id'],
        'permission_id': permissions[0]['id'],

    },
    {
        'id': '53e3def9-0f43-4a12-9b09-11d41c9ef993',
        'role_id': roles[0]['id'],
        'permission_id': permissions[1]['id'],
    },
    {
        'id': '0e2c0586-b5c1-4f7d-8f91-60fbc768619e',
        'role_id': roles[1]['id'],
        'permission_id': permissions[2]['id'],
    },
    {
        'id': '6ab0d632-505f-4e88-8e8c-0aecacba58ef',
        'role_id': roles[2]['id'],
        'permission_id': permissions[3]['id'],
    },
    {
        'id': '3567a87d-de25-46a7-b458-21be717cf953',
        'role_id': roles[2]['id'],
        'permission_id': permissions[4]['id'],
    }
]

users = [
    {
        'id': '3ddb563e-3158-4510-8347-17d86a541ec4',
        'username': 'user1',
        'pwd_hash': b'{\x91\xaa\x13\x91\xff4\xe0`I\xb7\\\xb7\xc8\tU2\x0c\x90Y\x13\x93d\x8b:\xa52w\x8e\x9c\x89\x98$$2b$12$ez50qzveKfpYkKlV78qmdu',
        'is_superuser': False,
        'data_joined': 1663523601,
        'terminate_date': 1663523602
    },
    {
        'id': '831d1a3b-6b00-420e-a460-1ea894487017',
        'username': 'user1',
        'pwd_hash': b'\xc9\x91+\x85\xdc\x16\xa3w\x8b+\x16QP\x1c\xcd\xe3.\xd6\xa0#\xfb\x08\xeank\x16N\xd7\xb2\xd0\xae\xa9$$2b$12$N7qvCbrFgtlol6OZMch1zu',
        'is_superuser': False,
        'data_joined': 1663523699,
        'terminate_date': 1663523600
    },
    {
        'id': '41c6bf7a-63d8-4341-ae6d-4fe1ddaea713',
        'username': 'user1',
        'pwd_hash': b"\xf0\xc5\x02\xf8\xef\x93S\xfe\xb8\x89\x9a\xd2'+\xa6\x8a \xa7z\x1b\xed\xb9P\xe3\xe0\xb3\xf3\xf8\x84z\xde'$$2b$12$yu7tYSkq1leRO4SySrTVKu",
        'is_superuser': False,
        'data_joined': 1663523698,
        'terminate_date': 1663523699
    }
]

users_roles = [
    {
        'id': '53e3def9-0f43-4a12-9b09-11d41c9ef993',
        'user_id': users[0]['id'],
        'role_id': roles[0]['id'],
    },
    {
        'id': '53e3def9-0f43-4a12-9b09-11d41c9ef993',
        'user_id': users[1]['id'],
        'role_id': roles[1]['id'],
    },
    {
        'id': '53e3def9-0f43-4a12-9b09-11d41c9ef993',
        'user_id': users[1]['id'],
        'role_id': roles[2]['id'],
    }
]
