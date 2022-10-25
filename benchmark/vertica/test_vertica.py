import random
import time
import vertica_python

from locust import TaskSet, task, User, between, events
from itertools import islice

from config import get_settings_instance

CONNECTION = {
    'host': get_settings_instance().HOST,
    'port': get_settings_instance().PORT,
    'user': get_settings_instance().USER,
    'password': get_settings_instance().PASSWORD,
    'database': get_settings_instance().DATABASE,
    'autocommit': get_settings_instance().AUTOCOMMIT,
    'read_timeout': get_settings_instance().READ_TIMEOUT,
    'unicode_error': get_settings_instance().UNICODE_ERROR,
    'ssl': get_settings_instance().SSL
}

wait_time_start = 0.1
wait_time_stop = 1


def group_elements(elements, chunk_size):
    """
        Группировка по чанкам
    """
    elements_to_group = iter(elements)
    return iter(lambda: tuple(islice(elements_to_group, chunk_size)), ())


def create_test_table(connection_info: dict) -> None:
    with vertica_python.connect(**connection_info) as connection:
        query = """
            CREATE TABLE IF NOT EXISTS views (
                id IDENTITY,
                user_id INTEGER NOT NULL,
                movie_id VARCHAR(256) NOT NULL,
                viewed_frame INTEGER NOT NULL
            );
        """
        cursor = connection.cursor()
        cursor.execute(query)


def generate_data_to_table(rows: int):
    return [(i, 'tt012033', i + 1) for i in range(rows)]


def delete_test_table(connection_info: dict) -> None:
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            DROP TABLE views;
        """)


def get_sample_query() -> str:
    random_id = random.randint(1, get_settings_instance().ROWS_NUMS)
    query = f"""
        SELECT * FROM views WHERE user_id = {random_id}
    """

    return query


def get_insert_query() -> str:

    query = """
        INSERT INTO views(user_id, movie_id, viewed_frame) VALUES(%s, %s, %s)
    """

    return query


def execute_query(conn_info, query, data, select=False) -> None:
    with vertica_python.connect(**conn_info) as conn:
        cur = conn.cursor()
        if select:
            cur.execute(query)
        else:
            cur.executemany(query, data, use_prepared_statements=False)


class VerticaClient:

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                execute_query(*args, **kwargs)
                events.request_success.fire(
                    request_type="vertica",
                    name=name,
                    response_time=int((time.time() - start_time) * 1000),
                    response_length=0,
                )
            except Exception as e:
                events.request_failure.fire(
                    request_type="vertica",
                    name=name,
                    response_time=int((time.time() - start_time) * 1000),
                    exception=e,
                )
        return wrapper


class VerticaTaskSet(TaskSet):

    @task(3)
    def execute_insert_query(self):
        for chunk_data in group_elements(
            generate_data_to_table(
                get_settings_instance().ROWS_NUMS
            ),
            get_settings_instance().CHUNK_SIZE
        ):
            self.client.execute_query(CONNECTION, get_insert_query(), chunk_data)

    @task
    def execute_select_query(self):
        self.client.execute_query(CONNECTION, get_sample_query(), [], select=True)


class VerticaLocust(User):
    tasks = [VerticaTaskSet]
    wait_time = between(
        wait_time_start,
        wait_time_stop
    )

    def __init__(self, environment):
        super().__init__(environment)
        self.client = VerticaClient()

    def on_start(self):
        create_test_table(CONNECTION)
