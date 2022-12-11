from __future__ import annotations

import fastapi

import src.models.http.healthcheck as http_healthcheck
from src.core.config import get_settings

router = fastapi.APIRouter(prefix='/api/v1/healthcheck')


@router.get(
    '/',
    response_model=http_healthcheck.Healthcheck,
    status_code=fastapi.status.HTTP_200_OK,
    description='Проверка статуса сервиса',
    summary='Endpoint позволяет проверить статус сервиса',
    tags=['Base'],
)
async def check_healthcheck(
        request: fastapi.Request,
        project_settings=fastapi.Depends(get_settings),
) -> http_healthcheck.Healthcheck:
    return http_healthcheck.Healthcheck(
        project_name=project_settings.project_name,
        version=request.app.version,
        health=True,
    )
