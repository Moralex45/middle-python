import typing

import src.models.broker as broker_mdl


class EventHandlerProtocol(typing.Protocol):

    message_model: type[broker_mdl.EventMessage]

    async def handle(self, message: broker_mdl.EventMessage) -> None:
        ...


class MessageHandlerProtocol(typing.Protocol):

    message_model: type[broker_mdl.PersonalizedMessage]

    async def handle(self, message: broker_mdl.PersonalizedMessage) -> None:
        ...
