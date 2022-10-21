import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.core.config import get_settings
from src.api.v1.events import router as events_router

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

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
