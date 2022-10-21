from fastapi import APIRouter, Request, Depends

from src.core.utils import verify_auth_tokens

router = APIRouter(prefix='/api/v1/events')


@router.post('/', dependencies=[Depends(verify_auth_tokens)])
async def film_search(request: Request):
    pass
