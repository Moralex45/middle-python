from __future__ import annotations

import logging

import src.core.settings as worker_settings
import src.handlers as handlers
import src.utils.aiomailing as mailing
import src.consumer as consumer
import src.utils.exceptions as exc

logger = logging.getLogger(__name__)


class Worker:
    def __init__(
        self,
        settings: worker_settings.MessageWorkerSettings,
        worker_consumer: consumer.ConsumerProtocol,
    ) -> None:
        self._settings = settings
        self._consumer = worker_consumer

    @classmethod
    async def from_settings(cls, settings: worker_settings.MessageWorkerSettings) -> Worker:
        logging.basicConfig(
            level=settings.LOGS_MIN_LEVEL,
            format=settings.LOGS_FORMAT,
        )

        logger.info('Initializing  message event_worker')

        logger.info('Initializing global clients')
        mailing_client = mailing.AioMailingSendgridClient(
            settings.mailing.api_key,
            settings.mailing.from_email,
        )

        logger.info('Initializing handlers')
        message_handler = handlers.PersonalizedMessageHandler(
            mailing_client,
            settings.templates,
        )

        logger.info('Initializing consumer')
        rabbitmq_consumer = consumer.RabbitmqConsumer(
            settings.rabbitmq.url,
            message_handler,
            queue_name=settings.rabbitmq.routing_key,
            login=settings.rabbitmq.username,
            password=settings.rabbitmq.password,
            prefetch_count=settings.rabbitmq.prefetch_count,
        )

        logger.info('Creating message event_worker')
        message_worker = Worker(
            settings=settings,
            worker_consumer=rabbitmq_consumer,
        )

        logger.info('Initializing of message event_worker finished')

        return message_worker

    async def start(self) -> None:
        await self.start_app()

    async def start_app(self) -> None:
        logger.info('Message event_worker is starting')

        try:
            await self._consumer.start_consuming()
        except BaseException as unexpected_error:
            logger.exception('Message event_worker failed to start')

            raise exc.StartWorkerError from unexpected_error

    async def dispose(self) -> None:
        logger.info('Message event_worker is shutting down...')

        dispose_errors = []

        logger.info('Disposing consumer')
        try:
            await self._consumer.dispose()
        except Exception as unexpected_error:  # noqa: PIE786
            dispose_errors.append(unexpected_error)
            logger.exception('Failed to dispose consumer')
        else:
            logger.info('Consumer has been disposed')

        if len(dispose_errors) != 0:
            logger.error('Message event_worker has shut down with errors')
            raise exc.DisposeError

        logger.info('Message event_worker has successfully shut down')


__all__ = [
    'Worker',
]
