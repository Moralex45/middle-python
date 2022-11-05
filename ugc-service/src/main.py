import asyncio

import uvicorn
import aiokafka
import fastapi
import sentry_sdk

import src.core.config as project_config
import src.api.v1.events as events_endpoints
import src.services.kafka as kafka_service

sentry_sdk.init(
    traces_sample_rate=1.0,
)

app = fastapi.FastAPI(
    title=project_config.get_settings().project_name,
    description='Сервиса для обработки активностей пользователя',
    version='0.1',
    redoc_url='/api/docs/redoc',
    docs_url='/api/docs/openapi',
    openapi_url='/api/docs/openapi.json',
    default_response_class=fastapi.responses.ORJSONResponse,
)

app.include_router(events_endpoints.router, tags=['events'])


@app.on_event('startup')
async def startup_event():
    loop = asyncio.get_event_loop()
    kafka_service.kafka_instance = aiokafka.AIOKafkaProducer(
        loop=loop,
        client_id=project_config.get_settings().project_name,
        bootstrap_servers=project_config.get_settings().kafka_settings.url,
    )
    await kafka_service.kafka_instance.start()


@app.on_event('shutdown')
async def shutdown_event():
    await kafka_service.kafka_instance.stop()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
