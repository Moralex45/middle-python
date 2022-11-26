import typing


class ConsumerProtocol(typing.Protocol):

    async def start_consuming(self) -> None:
        ...

    async def dispose(self) -> None:
        ...
