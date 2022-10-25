while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
done

cd src

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL

gunicorn --bind 0.0.0.0:8000 config.wsgi