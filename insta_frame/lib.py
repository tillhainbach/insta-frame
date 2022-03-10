"""Add a frame to any photo so it has format 1:1."""

from typing import Tuple

import cv2
import numpy as np

Image = np.ndarray[Tuple[int, int, int], np.dtype[np.uint8]]


def is_image(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[-1].lower() in ("jpeg", "jpg")


def string_data_to_image(data: bytes) -> Image:
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
