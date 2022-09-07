from dataclasses import dataclass

from multidict import CIMultiDictProxy
import pytest

from tests.functional.settings import get_settings_instance


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = get_settings_instance().BASE_API + '/api/v1' + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status
            )

    return inner
