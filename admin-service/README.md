# Запуск dev севера django

Создать env/.env.dev

docker run -d --rm --user 1000:1000 --name sprint2_postgres -p 54320:5432 --mount type=bind,source=$PWD/postgresql/init_scripts,target=/docker-entrypoint-initdb.d --mount type=volume,source=sprint2_pgdata,target=/var/lib/postgresql/data --env-file postgresql/env/.env.dev postgres:13

python3 01_docker_compose/load_data.py 01_docker_compose/.env
# Запуск docker-compose

1. Заполнить .env файлы. За основу взять рабочие .env.sample файлы

`app/env/.env.prod`; `postgresql/env/.env.prod`

2. Поднять сервисы

`docker-compose up --build`