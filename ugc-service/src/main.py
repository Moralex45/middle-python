import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import get_settings

app = FastAPI(
    title=get_settings().PROJECT_NAME,
    description='Сервиса для обработки активностей пользователя',
    version='0.1',
    redoc_url='/api/docs/redoc',
    docs_url='/api/docs/openapi',
    openapi_url='/api/docs/openapi.json',
    default_response_class=ORJSONResponse,
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
