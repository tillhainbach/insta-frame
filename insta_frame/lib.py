"""
Image utilities for InstaFrame.

Also includes wrappers around cv2 and numpy, so all image related function are
import from a single place.

"""

import base64
from typing import Callable, Tuple, TypeVar, overload

import cv2
import numpy as np

Image = np.ndarray[Tuple[int, int, int], np.dtype[np.uint8]]

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")
F = TypeVar("F")
G = TypeVar("G")


@overload
def pipe(_f1: Callable[[A], B], _f2: Callable[[B], C]) -> Callable[[A], C]:
    ...


@overload
def pipe(
    _f1: Callable[[A], B],
    _f2: Callable[[B], C],
    _f3: Callable[[C], D],
    _f4: Callable[[D], E],
    _f5: Callable[[E], F],
    _f6: Callable[[F], G],
) -> Callable[[A], G]:
    ...


def pipe(*_funcs):  # pyright: ignore
    def _pipe(value):
        for func in _funcs:
            value = func(value)
        return value

    return _pipe


def jpegify(image: Image) -> Image:
    return cv2.imencode(".jpg", image)[1]  # pyright: ignore


def as_b64(image: bytes) -> str:
    return base64.b64encode(image).decode()


def as_bytes(image: Image) -> bytes:
    return image.tobytes()


def as_url(image_b64: str, type: str = "jpeg") -> str:
    return f"data:image/{type};base64,{image_b64}"


def is_image(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[-1].lower() in ("jpeg", "jpg")


def from_bytes(data: bytes) -> Image:
    data_array = np.frombuffer(data, dtype=np.uint8)
    return cv2.imdecode(data_array, cv2.IMREAD_UNCHANGED)


def _create_white_bar(width: int, height: int) -> Image:
    white_pixel: Image = np.array([[[255, 255, 255]]])
    return np.tile(white_pixel, (height, width, 1))


def add_frame(to_image: Image) -> Image:
    height, width, _ = to_image.shape

    shape_difference = width - height
    if shape_difference == 0:  # is already in format 1:1.
        return to_image

    elif shape_difference < 0:
        # fill left and right side
        width_to_fill_on_each_side = int(shape_difference * -0.5)
        white_bar = _create_white_bar(width_to_fill_on_each_side, height)
        return np.hstack((white_bar, to_image, white_bar))

    else:  # shape_difference > 0
        # fill top and bottom
        height_to_file_on_top_and_bottom = int(shape_difference * 0.5)
        white_bar = _create_white_bar(width, height_to_file_on_top_and_bottom)
        return np.vstack((white_bar, to_image, white_bar))


def upload_image_pipe(data: bytes) -> str:
    return pipe(from_bytes, add_frame, jpegify, as_bytes, as_b64, as_url)(data)
