from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore
from apscheduler.jobstores.mongodb import MongoDBJobStore  # type: ignore
from apscheduler.executors.pool import ThreadPoolExecutor  # type: ignore

from src.core.config import get_settings
from src.models.storage.service_notification import ServiceNotification


def get_job_id(notification: ServiceNotification):
    if notification.type == 'like':
        # we need only one event for all review likes
        return notification.content.get('review_id')
    else:
        return notification.id


jobstores = {
    'mongo': MongoDBJobStore(database=get_settings().mongodb_settings.mongodb_database,
                             host=get_settings().mongodb_settings.host,
                             port=get_settings().mongodb_settings.port,
                             collection=get_settings().mongodb_settings.jobs_notifications_collection),
}
executors = {
    'default': ThreadPoolExecutor(20),
}

scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors)
