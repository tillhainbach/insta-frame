"""Backend Test Fixtures."""

import pytest
from flask import Flask

from insta_frame import create_app


@pytest.fixture
def app() -> Flask:
    """Get app in testing mode."""

    return create_app({"TESTING": True})


@pytest.fixture
def client(app: Flask):
    """Get test client."""
    return app.test_client()
