from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    status,
    Request
)

import src.models.http.healthcheck as http_healthcheck
from src.core.config import get_settings_instance

router = APIRouter(prefix='/api/v1/healthcheck')


@router.get(
    '/',
    response_model=http_healthcheck.Healthcheck,
    status_code=status.HTTP_200_OK,
    description='Проверка статуса сервиса',
    summary='Endpoint позволяет проверить статус сервиса',
    tags=['Base'],
)
async def check_healthcheck(
        request: Request,
        project_settings=Depends(get_settings_instance),
) -> http_healthcheck.Healthcheck:
    return http_healthcheck.Healthcheck(
        project_name=project_settings.project_name,
        version=request.app.version,
        health=True,
    )
