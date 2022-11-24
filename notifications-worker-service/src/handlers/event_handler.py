import logging

import src.models.broker as broker_mdl
import src.repositories as repo
import src.handlers.protocol as protocol
from src.core.settings import EventTypes

logger = logging.getLogger(__name__)


class EventHandler(protocol.EventHandlerProtocol):

    def __init__(self,
                 *,
                 review_repo: repo.ReviewRepositoryProtocol,
                 movie_users_repo: repo.MovieUsersRepositoryProtocol,
                 movies_repo: repo.MovieRepositoryProtocol,
                 users_repo: repo.UsersRepositoryProtocol,
                 broker_repo: repo.BrokerMessageRepositoryProtocol,
                 ) -> None:
        self.message_model = broker_mdl.EventMessage
        self._review_repo = review_repo
        self._movie_users_repo = movie_users_repo
        self._movies_repo = movies_repo
        self._users_repo = users_repo
        self._broker_repo = broker_repo

    async def handle(self, message: broker_mdl.EventMessage) -> None:
        match message.type:
            case EventTypes.LIKES:
                await self._handle_like(message)
            case EventTypes.MAILING:
                await self._handle_mass_mailing(message)
            case EventTypes.NEW_SERIES:
                await self._handle_new_series(message)
            case EventTypes.REGISTRATION:
                await self._handle_registration(message)

    async def _handle_like(self, message: broker_mdl.EventMessage) -> None:
        review_id = message.content.get('review_id')
        if review_id is None:
            logger.info('Broken message by id %s arrived', message.id)
            return
        review = await self._review_repo.get_review_by_id(review_id)
        user_info = await self._users_repo.get_user_by_id(review.user_id)
        movie_info = await self._movies_repo.get_movie_by_id(review.movie_id)
        content = {'movie_name': movie_info.title}
        message_to_sent = broker_mdl.PersonalizedMessage(id=message.id,
                                                         type=message.type,
                                                         email=user_info.email,
                                                         content=content)
        await self._broker_repo.publish_message(message_to_sent.json().encode())

    async def _handle_registration(self, message: broker_mdl.EventMessage) -> None:
        user_id = message.content.get('user_id')
        confirm_url = message.content.get('conf_url')
        if user_id is None or confirm_url is None:
            logger.info('Broken message by id %s arrived', message.id)
            return
        user_info = await self._users_repo.get_user_by_id(user_id)
        content = {'confirm_url': confirm_url}
        message_to_sent = broker_mdl.PersonalizedMessage(id=message.id,
                                                         type=message.type,
                                                         email=user_info.email,
                                                         content=content)
        await self._broker_repo.publish_message(message_to_sent.json().encode())

    async def _handle_new_series(self, message: broker_mdl.EventMessage) -> None:
        movie_id = message.content.get('movie_id')
        if movie_id is None:
            logger.info('Broken message by id %s arrived', message.id)
            return
        users_id = self._movie_users_repo.get_movie_viewers(movie_id)
        movie_info = await self._movies_repo.get_movie_by_id(movie_id)
        while cur_users_id := await anext(users_id):
            users = await self._users_repo.get_specified_users(cur_users_id)
            users_email = [user.email for user in users]
            content = {'movie_title': movie_info.title}
            for user_email in users_email:
                message_to_sent = broker_mdl.PersonalizedMessage(id=message.id,
                                                                 type=message.type,
                                                                 email=user_email,
                                                                 content=content)
                await self._broker_repo.publish_message(message_to_sent.json().encode())

    async def _handle_mass_mailing(self, message: broker_mdl.EventMessage) -> None:
        email_subject: str = message.content.get('subject', '')
        blocks: dict = message.content.get('blocks', {})
        if not email_subject or not blocks:
            logger.info('Broken message by id %s arrived', message.id)
            return
        users = self._users_repo.get_all_users()
        while cur_users := await anext(users):
            users_email = [user.email for user in cur_users]
            content = {'block1': blocks['block1'],
                       'block2': blocks['block2'],
                       'block3': blocks['block3']}
            for user_email in users_email:
                message_to_sent = broker_mdl.PersonalizedMessage(id=message.id,
                                                                 type=message.type,
                                                                 email=user_email,
                                                                 content=content)
                await self._broker_repo.publish_message(message_to_sent.json().encode())
