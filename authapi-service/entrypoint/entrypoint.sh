cd src

flask createdatabase
flask createdefault

gunicorn --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker asgi:asgi_app