import os

from insta_frame import create_app


def test_config() -> None:
    os.environ.update(SECRET_KEY="NOT-TESTING")
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing
