from insta_frame import create_app


def test_config() -> None:
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing
