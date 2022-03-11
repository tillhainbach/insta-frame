"""Backend Test Fixtures."""

import pytest
from quart import Quart

from insta_frame import create_app


@pytest.fixture
def app() -> Quart:
    """Get app in testing mode."""

    return create_app({"TESTING": True})


@pytest.fixture
def client(app: Quart):
    """Get test client."""
    return app.test_client()
