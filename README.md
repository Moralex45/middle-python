# Секция для ревьюера

Ссылка на гит-репозиторий проекта: 
https://github.com/M1LKYWVYs/Async_API_sprint_2

# Запуск тестов

В каждом модуле с тестами присутствует docker-compose файл для локального запуска тестов в контейнерах

`docker-compose --file docker-compose-test.yml up --build --abort-on-container-exit --remove-orphans`

# Запуск сервисов
`docker-compose --file docker-compose.yml up --build --remove-orphans`


# Инициализация проекта

# Инициализация рабочих проектов

1. Инициализировать корневую директорию как проект в IDE
2. Инициализировать директорию etl-service как проект в IDE
3. Инициализировать директорию asyncapi-service как проект в IDE
4. Инициализировать директорию authapi-service как проект в IDE
5. Инициализировать директорию admin-service как проект в IDE
6. Инициализировать директорию data-faker-service как проект в IDE
7. Заполнить postgresql/.env/.env.dev и postgresql/.env/.env.prod файлы окружения
8. Заполнить etl-service/.env/.env.dev и etl-service/.env/.env.prod файлы окружения
9. Заполнить asyncapi-service/tests/.env/.env.dev и asyncapi-service/tests/.env/.env.prod файлы окружения
10. Заполнить asyncapi-service/.env/.env.dev и asyncapi-service/.env/.env.prod файлы окружения
11. Заполнить data-faker/.env/.env.dev и data-faker/.env/.env.prod файлы окружения
12. Заполнить admin-service/.env/.env.dev и admin-service/.env/.env.prod файлы окружения

# Запуск postgres

`docker run -d --name sprint6_postgres -p 54320:5432 --mount type=bind,source=$PWD/postgresql/init_scripts,target=/docker-entrypoint-initdb.d --mount type=volume,source=sprint6_pgdata,target=/var/lib/postgresql/data --env-file postgresql/.env/.env.dev postgres:13`

После запуска postgres, необходимо инициализировать таблицы и заполнить их данными

# Запуск elastic

`docker run -d --name sprint6_elastic -p 9200:9200 --mount type=volume,source=sprint6_elasticsearch_data,target=/usr/share/elasticsearch/data  -e "discovery.type=single-node" elasticsearch:7.17.5`
