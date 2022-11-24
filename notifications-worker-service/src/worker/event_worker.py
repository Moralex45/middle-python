from __future__ import annotations

import logging

import aio_pika
import aiopg
import motor.motor_asyncio as motor_asyncio
import asynch  # type: ignore

import src.core.settings as worker_settings
import src.handlers as handlers
import src.consumer as consumer
import src.utils.exceptions as exc
import src.repositories as repo
import src.databases as db

logger = logging.getLogger(__name__)


class Worker:
    def __init__(
        self,
        settings: worker_settings.EventWorkerSettings,
        worker_consumer: consumer.ConsumerProtocol,
    ) -> None:
        self._settings = settings
        self._consumer = worker_consumer

    @classmethod
    async def from_settings(cls, settings: worker_settings.EventWorkerSettings) -> Worker:
        logging.basicConfig(
            level=settings.LOGS_MIN_LEVEL,
            format=settings.LOGS_FORMAT,
        )

        logger.info('Initializing event event_worker')

        logger.info('Initializing global clients')
        db.mongodb_instance = motor_asyncio.AsyncIOMotorClient(host=settings.mongo.host,
                                                               port=settings.mongo.port)

        logger.info('Opening the necessary connections')
        db.rabbitmq_instance = await aio_pika.connect(settings.rabbitmq.url,
                                                      connection_class=aio_pika.RobustConnection)
        db.clickhouse_connection = await asynch.connect(settings.clickhouse.url)
        db.auth_postgres_connection = await aiopg.connect(settings.auth_postgres.url)
        db.admin_postgres_connection = await aiopg.connect(settings.admin_postgres.url)

        logger.info('Initializing repositories')
        broker_repo = repo.BrokerMessageRabbitmqRepository(
            db.get_rabbitmq_instance(),
            routing_key=settings.rabbitmq.routing_key,
        )
        users_repo = repo.UsersPostgresRepository(
            db.get_postgres_connection(worker_settings.ServicesPostgres.AUTH),
            table_name=settings.auth_postgres.user_info_table_name,
            batch_size=settings.auth_postgres.batch_size,
        )
        reviews_repo = repo.ReviewMongoRepository(
            db.get_mongodb_instance(),
            database_name=settings.mongo.database,
            collection_name=settings.mongo.likes_collection,
        )
        movies_repo = repo.MoviePostgresRepository(
            db.get_postgres_connection(worker_settings.ServicesPostgres.ADMIN),
            table_name=settings.admin_postgres.movie_table_name,
        )
        movie_users_repo = repo.MovieUserClickhouseRepository(
            db.get_clickhouse_connection(),
            db_table=settings.clickhouse.db_table,
            batch_size=settings.clickhouse.batch_size,
        )

        logger.info('Initializing handlers')
        event_handler = handlers.EventHandler(
            review_repo=reviews_repo,
            users_repo=users_repo,
            movies_repo=movies_repo,
            broker_repo=broker_repo,
            movie_users_repo=movie_users_repo,
        )

        logger.info('Initializing consumer')
        rabbitmq_consumer = consumer.RabbitmqConsumer(
            settings.rabbitmq.url,
            event_handler,
            queue_name=settings.rabbitmq.routing_key,
            login=settings.rabbitmq.username,
            password=settings.rabbitmq.password,
            prefetch_count=settings.rabbitmq.prefetch_count,
        )

        logger.info('Creating event event_worker')
        message_worker = Worker(
            settings=settings,
            worker_consumer=rabbitmq_consumer,
        )

        logger.info('Initializing of event event_worker finished')

        return message_worker

    async def start(self) -> None:
        await self.start_app()

    async def start_app(self) -> None:
        logger.info('Event event_worker is starting')

        try:
            await self._consumer.start_consuming()
        except BaseException as unexpected_error:
            logger.exception('Event event_worker failed to start')

            raise exc.StartWorkerError from unexpected_error

    async def dispose(self) -> None:
        logger.info('Event event_worker is shutting down...')

        dispose_errors = []

        logger.info('Disposing consumer')
        try:
            await self._consumer.dispose()
        except Exception as unexpected_error:  # noqa: PIE786
            dispose_errors.append(unexpected_error)
            logger.exception('Failed to dispose consumer')
        else:
            logger.info('Consumer has been disposed')

        logger.info('Closing open connections')
        await db.get_postgres_connection(worker_settings.ServicesPostgres.ADMIN).close()
        await db.get_postgres_connection(worker_settings.ServicesPostgres.AUTH).close()
        await db.get_rabbitmq_instance().close()
        await db.get_clickhouse_connection().close()

        if len(dispose_errors) != 0:
            logger.error('Message event_worker has shut down with errors')
            raise exc.DisposeError

        logger.info('Message event_worker has successfully shut down')


__all__ = [
    'Worker',
]
