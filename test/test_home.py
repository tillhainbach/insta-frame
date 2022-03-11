"""Test home route."""


from typing import cast

from flask import Flask
from werkzeug import Response


def test_home_route(client: Flask) -> None:
    response = cast(Response, client.get("/"))

    assert response.status_code == 200
