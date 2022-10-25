roles = [
    {
        'id': '53877241-56a9-4c0e-92fb-57dfcfd63f8e',
        'code': 0,
        'description': 'admin'
    },
    {
        'id': 'de7e3e01-16b4-452d-83c8-837ea976c564',
        'code': 1,
        'description': 'user'
    },
    {
        'id': 'e42c19f9-41a8-4dcd-865d-c9c85d20ad85',
        'code': 2,
        'description': 'manager-manager-content-manager'
    },
]

permissions = [
    {
        'id': 'e0de2cb6-db6b-4e03-8426-e74eac73801a',
        'code': 0,
    },
    {
        'id': 'd48f6bb1-c060-49da-a9b0-d04af161b7ed',
        'code': 1,
    },
    {
        'id': 'aafebc0a-6396-4f9d-bfca-51089df12319',
        'code': 2,
    },
    {
        'id': '175d8060-d108-4898-af38-ffc4000027fc',
        'code': 3,
    },
    {
        'id': '7a11716c-819d-4929-866d-d5093fd253a2',
        'code': 4,
    }
]

roles_permissions = [
    {
        'id': '809378b2-c567-4c83-a4c8-120768787abf',
        'role_id': roles[1]['id'],
        'permission_id': permissions[4]['id'],

    },
    {
        'id': '53e3def9-0f43-4a12-9b09-11d41c9ef993',
        'role_id': roles[0]['id'],
        'permission_id': permissions[0]['id'],
    },
    {
        'id': '0e2c0586-b5c1-4f7d-8f91-60fbc768619e',
        'role_id': roles[0]['id'],
        'permission_id': permissions[1]['id'],
    },
    {
        'id': '6ab0d632-505f-4e88-8e8c-0aecacba58ef',
        'role_id': roles[0]['id'],
        'permission_id': permissions[2]['id'],
    },
    {
        'id': '3567a87d-de25-46a7-b458-21be717cf953',
        'role_id': roles[0]['id'],
        'permission_id': permissions[3]['id'],
    }
]

users = [
    {
        'id': '3ddb563e-3158-4510-8347-17d86a541ec4',
        'username': 'user1',
        'password': 'pwd1',
    },
    {
        'id': '831d1a3b-6b00-420e-a460-1ea894487017',
        'username': 'user2',
        'password': 'pwd2',
    },
    {
        'id': '41c6bf7a-63d8-4341-ae6d-4fe1ddaea713',
        'username': 'user3',
        'password': 'pwd3',
    }
]

super_users = [
    {
        'id': '41c6bf7a-63d8-4341-ae6d-4fe1ddaea731',
        'username': 'iamroot',
        'password': 'pwd1',
        'is_superuser': True
    }
]

users_roles = [
    {
        'id': 'fdc27267-0a23-4594-be76-c94ff9e2aa09',
        'user_id': users[0]['id'],
        'role_id': roles[0]['id'],
    },
    {
        'id': '4558db65-2a68-453a-a572-9396ec9b17bd',
        'user_id': users[1]['id'],
        'role_id': roles[1]['id'],
    },
    {
        'id': '67ff5328-f6da-4bb2-872a-285da7c360fc',
        'user_id': users[1]['id'],
        'role_id': roles[2]['id'],
    }
]

user_agents = ['Chrome', 'Safari', 'Opera']
