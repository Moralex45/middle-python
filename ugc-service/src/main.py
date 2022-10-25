import asyncio

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.core.config import get_settings
from src.api.v1.events import router as events_router
from src.storages import kafka

app = FastAPI(
    title=get_settings().PROJECT_NAME,
    description='Сервиса для обработки активностей пользователя',
    version='0.1',
    redoc_url='/api/docs/redoc',
    docs_url='/api/docs/openapi',
    openapi_url='/api/docs/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(events_router, tags=['events'])


@app.on_event('startup')
async def startup_event():
    loop = asyncio.get_event_loop()
    kafka.producer = AIOKafkaProducer(
        loop=loop,
        client_id=get_settings().PROJECT_NAME,
        bootstrap_servers=get_settings().kafka_settings.url,
    )
    await kafka.producer.start()


@app.on_event('shutdown')
async def shutdown_event():
    await kafka.producer.stop()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
