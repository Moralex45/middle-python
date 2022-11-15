# Секция для ревьюера

Ссылка на гит-репозиторий проекта: 
https://github.com/KenKi2002/ugc_sprint_1  


# Запуск тестов

В каждом модуле с тестами присутствует docker-compose файл для локального запуска тестов в контейнерах

`docker-compose --file docker-compose-test.yml up --build --abort-on-container-exit --remove-orphans`

# Запуск сервисов

`docker-compose --file docker-compose.yml up --build --remove-orphans`


# Инициализация проекта

# Инициализация рабочих проектов

* Инициализировать корневую директорию как проект в IDE
* Инициализировать директорию etl-service как проект в IDE
* Инициализировать директорию asyncapi-service как проект в IDE
* Инициализировать директорию ugc-service как проект в IDE
* Инициализировать директорию ugc-extra-service как проект в IDE
* Инициализировать директорию notifications-service как проект в IDE
* Инициализировать директорию etl-kafka-clickhouse как проект в IDE
* Инициализировать директорию authapi-service как проект в IDE
* Инициализировать директорию admin-service как проект в IDE
* Инициализировать директорию data-faker-service как проект в IDE
* Заполнить docker/auth_postgresql/.env/.env.dev и docker/auth_postgresql/.env/.env.prod файлы окружения
* Заполнить docker/movies_postgresql/.env/.env.dev и docker/movies_postgresql/.env/.env.prod файлы окружения
* Заполнить etl-service/.env/.env.dev и etl-service/.env/.env.prod файлы окружения
* Заполнить asyncapi-service/tests/.env/.env.dev и asyncapi-service/tests/.env/.env.prod файлы окружения
* Заполнить asyncapi-service/.env/.env.dev и asyncapi-service/.env/.env.prod файлы окружения
* Заполнить ugc-service/.env/.env.dev и ugc-service/.env/.env.prod файлы окружения
* Заполнить ugc-extra-service/.env/.env.dev и ugc-extra-service/.env/.env.prod файлы окружения
* Заполнить notifications-service/.env/.env.dev и notifications-service/.env/.env.prod файлы окружения
* Заполнить etl-kafka-clickhouse/.env/.env.dev и etl-kafka-clickhouse/.env/.env.prod файлы окружения
* Заполнить authapi-service/.env/.env.dev и authapi-service/.env/.env.prod файлы окружения
* Заполнить data-faker/.env/.env.dev и data-faker/.env/.env.prod файлы окружения
* Заполнить admin-service/.env/.env.dev и admin-service/.env/.env.prod файлы окружения

# Запуск postgres

`docker run -d --name yp_movies_postgres -p 54320:5432 --mount type=bind,source=$PWD/docker/movies_postgresql/init_scripts,target=/docker-entrypoint-initdb.d --mount type=volume,source=sprint7_movies_pgdata,target=/var/lib/postgresql/data --env-file docker/movies_postgresql/.env/.env.dev postgres:13`

`docker run -d --name yp_auth_postgres -p 54321:5432 --mount type=bind,source=$PWD/docker/auth_postgresql/init_scripts,target=/docker-entrypoint-initdb.d --mount type=volume,source=sprint7_auth_pgdata,target=/var/lib/postgresql/data --env-file docker/auth_postgresql/.env/.env.dev postgres:13`

После запуска postgres, необходимо инициализировать таблицы и заполнить их данными

# Запуск elastic

`docker run -d --name yp_elastic -p 9200:9200 -e "discovery.type=single-node" elasticsearch:7.17.5`


# Запуск redis

`docker run -d --name yp_movies_redis -p 63790:6379 redis`

`docker run -d --name yp_auth_redis -p 63791:6379 redis`

`docker run -d --name yp_ugc_redis -p 63792:6379 redis`

`docker run -d --name yp_ugc_extra_redis -p 63793:6379 redis`

# Запуск kafka

https://developer.confluent.io/quickstart/kafka-docker

# Запуск MongoDB

`docker run -d --name yp_ugc_mongo -p 270170:27017 mongo`

`docker run -d --name yp_notifcations_mongo -p 270171:27017 mongo`