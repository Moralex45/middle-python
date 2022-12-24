import fastapi
import uvicorn

from src.core.config import get_settings_instance
from src.api.v1 import healthcheck as healthcheck_routing
from src.api.v1 import payment_refund as payment_refund_routing
from src.api.v1 import payment as payment_routing
from src.api.v1 import subscription as subscription_routing

app = fastapi.FastAPI(
    title=get_settings_instance().PROJECT_NAME,
    description='User-purchase-service',
    version='0.1',
    redoc_url='/api/docs/redoc',
    docs_url='/api/docs/openapi',
    openapi_url='/api/docs/openapi.json',
    default_response_class=fastapi.responses.ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    ...


@app.on_event('shutdown')
async def shutdown():
    ...


app.include_router(healthcheck_routing.router)
app.include_router(payment_refund_routing.router)
app.include_router(payment_routing.router)
app.include_router(subscription_routing.router)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
