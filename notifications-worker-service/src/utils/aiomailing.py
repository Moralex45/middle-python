import typing

import aiosendgrid  # type: ignore
from sendgrid.helpers.mail import Content, Mail, From, To  # type: ignore

import src.utils.exceptions as exc


class AioMailingClientProtocol(typing.Protocol):

    async def send_email(self, to: str, subject: str, content: str) -> None:
        """
        :raises SendEmailFailError: if failed to send email
        """
        ...

    async def send_many(self, to: list[str], subject: str, content: str) -> None:
        """
        :raises SendEmailFailError: if failed to send email, failed recipient in exception message
        """
        ...


class AioMailingSendgridClient(AioMailingClientProtocol):

    def __init__(self,
                 api_key: str,
                 from_: str) -> None:
        self._client = aiosendgrid.AsyncSendGridClient(api_key=api_key)
        self._from_email = From(from_)

    async def send_email(self, to: str, subject: str, content: str) -> None:
        """
        :param to: recipient email address
        :param subject: email message subject
        :param content: email message body
        """
        mail = await self._prepare_email(to, subject, content)
        async with self._client as client:
            response = await client.send_mail_v3(body=mail.get())
            if response.status_code >= 300:
                raise exc.SendEmailFailError

    async def send_many(self, to: list[str], subject: str, content: str) -> None:
        """
        :param to: list of recipients email addresses
        :param subject: email message subject
        :param content: email message body
        """
        mails = [await self._prepare_email(to_email, subject, content) for to_email in to]
        async with self._client as client:
            for mail in mails:
                response = await client.send_mail_v3(body=mail.get())
                if response.status_code >= 300:
                    raise exc.SendEmailFailError(to)

    async def _prepare_email(self, to: str, subject: str, content: str) -> Mail:
        to_email = To(to)
        email_content = Content('text/html', content)
        return Mail(self._from_email, to_email, subject, email_content)
