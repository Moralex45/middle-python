# Секция для ревьюера

Ссылка на гит-репозиторий проекта: 
https://github.com/M1LKYWVYs/Async_API_sprint_2

# Запуск тестов
`docker-compose -p async_api_sprint_tests --file docker-compose-test.yml up --build --abort-on-container-exit --remove-orphans`

# Запуск сервисов
`docker-compose --file docker-compose.yml up --build`


# Инициализация проекта

# Инициализация рабочих проектов fastapi и etl

1. Инициализировать корневую директорию как проект в IDE
2. Инициализировать директорию etl как проект в IDE
3. Инициализировать директорию fastapi как проект в IDE
4. Заполнить postgresql/.env/.env.dev и postgresql/.env/.env.prod файлы окружения
5. Заполнить etl/.env/.env.dev и etl/.env/.env.prod файлы окружения
6. Заполнить fastapi/.env/.env.dev и fastapi/.env/.env.prod файлы окружения

# Запуск postgres

`docker run -d --name sprint4_postgres -p 54320:5432 --mount type=bind,source=$PWD/postgresql/init_scripts,target=/docker-entrypoint-initdb.d --mount type=volume,source=sprint4_pgdata,target=/var/lib/postgresql/data --env-file postgresql/.env/.env.dev postgres:13`

После запуска postgres, необходимо инициализировать таблицы и заполнить их данными

# Запуск elastic

`docker run -d --name sprint4_elastic -p 9200:9200 --mount type=volume,source=sprint4_elasticsearch_data,target=/usr/share/elasticsearch/data  -e "discovery.type=single-node" elasticsearch:7.17.5`
