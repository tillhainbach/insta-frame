"""Test suite for insta-frame."""

from syrupy.assertion import SnapshotAssertion

from insta_frame.lib import Image, add_frame, is_image, jpegify


def test_add_frame(image) -> None:
    image_ut = add_frame(image)

    height_ut, width_ut, dim_ut = image_ut.shape
    height, width, dim = image.shape

    assert width_ut == height_ut
    assert dim == dim_ut
    if height > width:
        assert height == height_ut
    else:
        assert width == width_ut


def test_is_image() -> None:
    assert is_image("linientreu.jpg")
    assert not is_image("linientreu")


def test_snapshot(image: Image, jpeg_snapshot: SnapshotAssertion) -> None:
    sut = add_frame(image)

    assert jpegify(sut).tobytes() == jpeg_snapshot
