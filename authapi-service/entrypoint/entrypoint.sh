while ! nc -z $POSTGRES_DB_HOST $POSTGRES_DB_PORT; do
      sleep 0.1
done

cd src

flask createdatabase
flask createdefault

gunicorn --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker asgi:asgi_app