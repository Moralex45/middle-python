import fastapi
import sentry_sdk
import uvicorn

import src.api.v1.healthcheck as healthcheck_routing
import src.core.config as project_config

app = fastapi.FastAPI(
    title=project_config.get_settings().project_name,
    description='Сервис обработки событий нотификации',
    version='0.1',
    redoc_url='/api/docs/redoc',
    docs_url='/api/docs/openapi',
    openapi_url='/api/docs/openapi.json',
    default_response_class=fastapi.responses.ORJSONResponse,
)

app.include_router(healthcheck_routing.router, tags=['healthcheck'])


@app.on_event('startup')
async def startup_event():
    if not project_config.get_settings().debug:
        sentry_sdk.init(dsn=project_config.get_settings().sentry_settings.dsn)

        # TODO implement opening connections
        ...


@app.on_event('shutdown')
async def shutdown_event():
    # TODO implement closing connections
    ...


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
