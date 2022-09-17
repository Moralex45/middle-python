import uuid

from app_utils import create_app
from db.services import role_permission_service


def main():
    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    main()
