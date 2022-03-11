"""Test home route."""

from typing import cast

import pytest
from quart import Quart
from werkzeug import Response


@pytest.mark.asyncio
async def test_home_route(client: Quart) -> None:
    response = cast(Response, await client.get("/"))  # type: ignore

    assert response.status_code == 200
