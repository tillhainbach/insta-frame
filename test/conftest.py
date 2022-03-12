"""Backend Test Fixtures."""

from pathlib import Path

import cv2
import numpy
import pytest
from quart import Quart
from quart.testing import QuartClient
from syrupy.assertion import SnapshotAssertion

from insta_frame import create_app

from .snapshot_extensions import HTMLImageSnapshotExtension, JPEGImageSnapshotExtension


@pytest.fixture
def app() -> Quart:
    """Get app in testing mode."""

    return create_app({"TESTING": True, "SECRET_KEY": "testing"})


@pytest.fixture
def client(app: Quart) -> QuartClient:
    """Get test client."""
    return app.test_client()


@pytest.fixture
def html_snapshot(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot(extension_class=HTMLImageSnapshotExtension)


@pytest.fixture
def jpeg_snapshot(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot(extension_class=JPEGImageSnapshotExtension)


def read_fixture(name: str) -> numpy.ndarray:
    filepath = Path(__file__).parent / "__fixtures__" / name
    if not filepath.exists:
        raise FileExistsError(f"Can't open file {filepath}!")
    return cv2.imread(str(filepath))


@pytest.fixture(params=["cat.jpg", "puppy.jpg", "cat_square.jpeg"])
def image(request) -> numpy.ndarray:
    return read_fixture(request.param)
