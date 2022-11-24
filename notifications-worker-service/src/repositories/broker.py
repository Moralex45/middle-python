import typing

import aio_pika
import aio_pika.abc as aio_pika_abc


class BrokerMessageRepositoryProtocol(typing.Protocol):

    async def publish_message(self, body: bytes) -> None:
        ...


class BrokerMessageRabbitmqRepository(BrokerMessageRepositoryProtocol):
    def __init__(
            self,
            connection: aio_pika_abc.AbstractConnection,
            *,
            routing_key: str,
    ):
        self._routing_key = routing_key
        self.__connection = connection

    async def publish_message(self, body: bytes) -> None:
        async with self.__connection as conn:
            channel = await conn.channel()

            await channel.default_exchange.publish(
                aio_pika.Message(body=body),
                routing_key=self._routing_key,
            )
