roles = [
    {
        'id': '53877241-56a9-4c0e-92fb-57dfcfd63f8e',
        'code': 1,
        'description': 'content-manager'
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
    }
]

roles_permissions = [
    {
        'id': '809378b2-c567-4c83-a4c8-120768787abf',
        'role_id': roles[0]['id'],
        'perm_id': permissions[0]['id'],

    },
    {
        'id': '53e3def9-0f43-4a12-9b09-11d41c9ef993',
        'role_id': roles[0]['id'],
        'perm_id': permissions[1]['id'],

    }
]
