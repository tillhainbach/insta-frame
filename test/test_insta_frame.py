"""Test suite for insta-frame."""

from pathlib import Path

import cv2
import numpy

from insta_frame.lib import add_frame, is_image


def test_add_frame() -> None:
    image = cv2.imread(str(Path(__file__).parent / "__fixtures__/cat.jpg"))

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


def test_snapshot(tmp_path: Path) -> None:
    image = cv2.imread(str(Path(__file__).parent / "__fixtures__/cat.jpeg"))

    sut = add_frame(image)

    name = __name__.rsplit(".", 1)[-1]

    assert_snapshot(sut, f"{name}_0", tmp_path)


def assert_snapshot(data, name: str, tmp_path: Path) -> None:
    _snapshots = Path(__file__).parent / "__snapshots__"
    if not _snapshots.exists():
        _snapshots.mkdir()
    snapshot = _snapshots.joinpath(f"{name}.jpeg")

    if not snapshot.exists():
        cv2.imwrite(str(snapshot), data)
        assert False, "No snapshot available, created new snapshot. Please run again!"

    snapshot_data = cv2.imread(str(snapshot))
    sut_path = tmp_path.joinpath("sut.jpeg")
    cv2.imwrite(str(sut_path), data)
    sut_jpeg = cv2.imread(str(sut_path))

    if not numpy.array_equal(snapshot_data, sut_jpeg):
        diff = tmp_path.joinpath(f"{name}_diff.jpeg")
        cv2.imwrite(str(diff), snapshot_data - data)
        assert False, (
            "snapshots did not match!\n"
            f"Call \n`open {diff}`\nto see diff.\n"
            f"Call \n`open {sut_path}`\n to see output.\n"
        )

    assert True
