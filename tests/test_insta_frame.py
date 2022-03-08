"""Test suite for insta-frame."""

from pathlib import Path

import cv2
import numpy

from insta_frame.lib import add_frame, is_image


def test_add_frame() -> None:
    image = cv2.imread("./resources/linientreu.jpg")

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


def test_screenshot(tmp_path: Path) -> None:
    image = cv2.imread("./resources/linientreu.jpg")

    sut = add_frame(image)

    assert_screenshot(sut, f"{__name__}_0", tmp_path)


def assert_screenshot(data, name: str, tmp_path: Path) -> None:
    _screenshots = Path(__file__).parent.joinpath("__screenshots__")
    if not _screenshots.exists():
        _screenshots.mkdir()
    screenshot = _screenshots.joinpath(f"{name}.jpeg")

    if not screenshot.exists():
        print(screenshot)
        cv2.imwrite(str(screenshot), data)
        assert (
            False
        ), "No screenshot available, created new screenshot. Please run again!"

    screenshot_data = cv2.imread(str(screenshot))
    sut_path = tmp_path.joinpath("sut.jpeg")
    cv2.imwrite(str(sut_path), data)
    sut_jpeg = cv2.imread(str(sut_path))

    if not numpy.array_equal(screenshot_data, sut_jpeg):
        diff = tmp_path.joinpath(f"{name}_diff.jpeg")
        cv2.imwrite(str(diff), screenshot_data - data)
        assert False, (
            "Screenshots did not match!\n"
            f"Call \n`open {diff}`\nto see diff.\n"
            f"Call \n`open {sut_path}`\n to see output.\n"
        )

    assert True
