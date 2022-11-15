import aio_pika
import fastapi
import uvicorn
from motor import motor_asyncio
import sentry_sdk

import src.core.config as project_config
import src.services.storage as storage_service
import src.services.amqp as amqp_service


if not project_config.get_settings().debug:
    sentry_sdk.init()

app = fastapi.FastAPI(
    title=project_config.get_settings().project_name,
    description='Сервис обработки событий нотификации',
    version='0.1',
    redoc_url='/api/docs/redoc',
    docs_url='/api/docs/openapi',
    openapi_url='/api/docs/openapi.json',
    default_response_class=fastapi.responses.ORJSONResponse,
)


@app.on_event('startup')
async def startup_event():
    storage_service.mongodb.mongodb_instance = motor_asyncio.AsyncIOMotorClient(
        host=project_config.get_settings().mongodb_settings.host,
        port=project_config.get_settings().mongodb_settings.port,
    )

    amqp_service.rabbitmq.rabbitmq_connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )



if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
