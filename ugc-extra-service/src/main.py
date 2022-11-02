import uvicorn
import fastapi

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
    pass


@app.on_event('shutdown')
async def shutdown_event():
    pass


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
