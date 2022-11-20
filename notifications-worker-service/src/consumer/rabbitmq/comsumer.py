import asyncio

from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage, AbstractConnection, AbstractRobustConnection

import src.models.broker as broker_models
import src.handler as msg_handler


class Consumer:

    def __init__(self,
                 url: str,
                 message_handler: msg_handler.MessageHandlerProtocol | None,
                 *,
                 queue_name: str,
                 login: str = 'guest',
                 password: str = 'guest') -> None:
        self.connection_url = url
        self.queue_name = queue_name
        self.message_handler = message_handler
        self.__login = login
        self.__password = password
        self.connection: AbstractRobustConnection | None = None

    async def init_connection(self) -> AbstractConnection:
        return await connect_robust(url=self.connection_url, login=self.__login, password=self.__password)

    async def on_message(self, message: AbstractIncomingMessage) -> None:
        async with message.process():
            event = broker_models.Message.parse_raw(message.body.decode('utf-8'))
            await self.message_handler.handle(event)

    async def start_consuming(self) -> None:
        self.connection = await self.init_connection()

        async with self.connection as conn:
            channel = await conn.channel()
            await channel.set_qos(prefetch_count=1)
            queue = await channel.get_queue(self.queue_name, ensure=True)
            await queue.consume(self.on_message)
            await asyncio.Future()

    async def dispose(self) -> None:
        await self.connection.close()
