FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY poetry.lock pyproject.toml /opt/app/
COPY entrypoint/entrypoint.sh .

RUN mkdir -p /var/www/static/  \
    && mkdir -p /var/www/media/  \
    && mkdir -p /opt/app/static/  \
    && mkdir -p /opt/app/media/  \
    && apt install gcc \
    && pip install --upgrade pip  \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install \
    && chmod a+x entrypoint.sh  \
    && apt update  \
    && apt install -y netcat

COPY src src

ENTRYPOINT ["sh", "entrypoint.sh"]
