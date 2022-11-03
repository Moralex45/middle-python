import uvicorn
import fastapi
from motor import motor_asyncio

import src.services.storage as storage_service
import src.core.config as project_config


app = fastapi.FastAPI(
    title=project_config.get_settings().project_name,
    description='Сервис обработки событий пользовательской активности',
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


@app.on_event('shutdown')
async def shutdown_event():
    ...


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
