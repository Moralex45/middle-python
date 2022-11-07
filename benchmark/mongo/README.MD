Тестирование хранилища MongoDB

Железо на котором производилось тестирование
CPU - Intel Core i3-1005G1 1.20Ghz*4
16RAM

# Запуск
Запустить инфраструктуру

    make start

Выполнить первоначальную настройку
    
    make db-init

Тестирование

    make full-test

## Результат pytest

    ======================================== test session starts ========================================
    platform linux -- Python 3.10.7, pytest-7.1.2, pluggy-1.0.0 -- /home/moralex/Projects/2/ugc_sprint_2/storage_test/mongo/venv/bin/python
    cachedir: .pytest_cache
    rootdir: /home/moralex/Projects/3/ugc_sprint_2/storage_test/Mongo/tests, configfile: pytest.ini
    plugins: asyncio-0.18.3, Faker-14.1.0
    asyncio: mode=auto
    collected 12 items                                                                                  

    tests/mongo_test.py::test_insert_movies_likes[10000] Fill likes collection. 10000 docs. 
    PASSED	Inserted docs | 10000 | 100%
    tests/mongo_test.py::test_insert_movies_likes[100000] Fill likes collection. 100000 docs. 
    PASSED	Inserted docs | 100000 | 100%
    tests/mongo_test.py::test_insert_movies_likes[1000000] Fill likes collection. 1000000 docs. 
    PASSED	Inserted docs | 1000000 | 100%
    tests/mongo_test.py::test_insert_review_likes PASSED
    tests/mongo_test.py::test_insert_bookmarks[100] PASSED
    tests/mongo_test.py::test_insert_bookmarks[1000] PASSED
    tests/mongo_test.py::test_insert_bookmarks[10000] PASSED
    tests/mongo_test.py::test_top_movies[10] PASSED
    tests/mongo_test.py::test_top_movies[100] PASSED
    tests/mongo_test.py::test_top_movies[1000] PASSED
    tests/mongo_test.py::test_film_ratings PASSED
    tests/mongo_test.py::test_user_bookmarks PASSED

    ========================================= slowest durations =========================================
    3647.30s call     mongo_test.py::test_insert_movies_likes[1000000]
    355.64s call     mongo_test.py::test_insert_movies_likes[100000]
    58.89s call     mongo_test.py::test_insert_review_likes
    39.35s call     mongo_test.py::test_insert_bookmarks[10000]
    16.78s call     mongo_test.py::test_insert_movies_likes[10000]
    4.02s call     mongo_test.py::test_insert_bookmarks[1000]
    1.78s call     mongo_test.py::test_top_movies[1000]
    1.68s call     mongo_test.py::test_top_movies[10]
    1.47s call     mongo_test.py::test_top_movies[100]
    0.99s setup    mongo_test.py::test_film_ratings
    0.62s setup    mongo_test.py::test_insert_movies_likes[10000]
    0.39s call     mongo_test.py::test_insert_bookmarks[100]
    0.22s call     mongo_test.py::test_film_ratings
    0.01s setup    mongo_test.py::test_user_bookmarks
    0.01s teardown mongo_test.py::test_user_bookmarks
    0.00s call     mongo_test.py::test_user_bookmarks
    0.00s setup    mongo_test.py::test_insert_movies_likes[1000000]
    0.00s setup    mongo_test.py::test_insert_bookmarks[10000]
    0.00s setup    mongo_test.py::test_top_movies[10]
    0.00s setup    mongo_test.py::test_insert_bookmarks[100]
    0.00s setup    mongo_test.py::test_insert_bookmarks[1000]
    0.00s setup    mongo_test.py::test_insert_review_likes
    0.00s setup    mongo_test.py::test_insert_movies_likes[100000]
    0.00s teardown mongo_test.py::test_insert_bookmarks[10000]
    0.00s teardown mongo_test.py::test_insert_movies_likes[100000]
    0.00s setup    mongo_test.py::test_top_movies[1000]
    0.00s teardown mongo_test.py::test_insert_bookmarks[100]
    0.00s setup    mongo_test.py::test_top_movies[100]
    0.00s teardown mongo_test.py::test_insert_bookmarks[1000]
    0.00s teardown mongo_test.py::test_insert_movies_likes[1000000]
    0.00s teardown mongo_test.py::test_insert_review_likes
    0.00s teardown mongo_test.py::test_insert_movies_likes[10000]
    0.00s teardown mongo_test.py::test_top_movies[100]
    0.00s teardown mongo_test.py::test_top_movies[10]
    0.00s teardown mongo_test.py::test_top_movies[1000]
    0.00s teardown mongo_test.py::test_film_ratings
    ================================== 12 passed in 4129.17s (1:08:49) ==================================

