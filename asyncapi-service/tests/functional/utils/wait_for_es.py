import logging
import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

from tools import backoff

logging.basicConfig(level=logging.ERROR)

load_dotenv()


def elasticsearch_connection_url() -> str:
    elastic_host: str = os.environ.get('ELASTIC_HOST', default='127.0.0.1')
    elastic_port: int = int(os.environ.get('ELASTIC_PORT', default=9200))
    return f'http://{elastic_host}:{elastic_port}'


@backoff()
def ping_es(es_client: Elasticsearch) -> bool:
    return es_client.info()


def wait_for_es():
    es_client: Elasticsearch = Elasticsearch(hosts=[elasticsearch_connection_url()])
    try:
        ping_es(es_client)
        logging.info('ES successfully awaited.')
    except Exception:
        logging.error('Unable to ping ES. Aborting.')
    es_client.close()


if __name__ == '__main__':
    wait_for_es()
