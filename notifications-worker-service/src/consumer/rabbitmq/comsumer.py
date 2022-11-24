import asyncio

from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustConnection

import src.handlers.protocol as handler_protocol
import src.utils.exceptions as exc
from src.consumer.protocol import ConsumerProtocol


class RabbitmqConsumer(ConsumerProtocol):

    def __init__(self,
                 url: str,
                 message_handler: handler_protocol.EventHandlerProtocol | handler_protocol.MessageHandlerProtocol,
                 *,
                 queue_name: str,
                 login: str = 'guest',
                 password: str = 'guest',
                 prefetch_count: int = 1) -> None:
        self.connection_url = url
        self.queue_name = queue_name
        self.message_handler = message_handler
        self.prefetch_count = prefetch_count
        self.__login = login
        self.__password = password
        self.__connection: AbstractRobustConnection | None = None

    async def __init_connection(self) -> AbstractRobustConnection:
        return await connect_robust(url=self.connection_url, login=self.__login, password=self.__password)

    async def __on_message(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            event = self.message_handler.message_model.parse_raw(message.body.decode('utf-8'))
            try:
                await self.message_handler.handle(event)
                await message.ack()
            except exc.MessageHandlingError:
                await message.reject(requeue=True)

    async def start_consuming(self) -> None:
        self.__connection = await self.__init_connection()

        async with self.__connection as conn:
            channel = await conn.channel()
            await channel.set_qos(prefetch_count=self.prefetch_count)
            queue = await channel.get_queue(self.queue_name, ensure=True)
            await queue.consume(self.__on_message)
            await asyncio.Future()

    async def dispose(self) -> None:
        await self.__connection.close()
