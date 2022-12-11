import aiofiles
import logging
from jinja2 import Template

import src.models.broker as broker_mdl
import src.utils.exceptions as exc
import src.handlers.protocol as protocol
from src.core.settings import TemplatesSettings
from src.utils.aiomailing import AioMailingClientProtocol


logger = logging.getLogger(__name__)


class PersonalizedMessageHandler(protocol.MessageHandlerProtocol):

    def __init__(self,
                 mailing: AioMailingClientProtocol,
                 template_settings: TemplatesSettings,
                 ) -> None:
        self.message_model = broker_mdl.PersonalizedMessage
        self._mailing = mailing
        self._template_settings = template_settings

    async def handle(self, message: broker_mdl.PersonalizedMessage) -> None:
        async with aiofiles.open(self._template_settings.get_templates_path(message.type), mode='r') as f:
            template = Template(await f.read())
        rendered_template = await template.render_async(message.content)
        try:
            await self._mailing.send_email(message.email,
                                           self._template_settings.get_subject(message.type),
                                           rendered_template)
        except exc.SendEmailFailError as ex:
            logger.info('Failed to send email to %s', message.email, exc_info=ex)
            raise exc.MessageHandlingError from ex
