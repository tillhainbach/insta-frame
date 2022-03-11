"""Home View."""

import typing

import cv2
from quart import Blueprint, current_app, flash, jsonify, render_template, request
from quart.wrappers.response import Response
from werkzeug.datastructures import FileStorage

from insta_frame.lib import add_frame, as_b64, as_url, is_image, string_data_to_image

bp = Blueprint("home", __name__)


@bp.route("/?", methods=["POST"])
async def upload_image() -> Response:
    files: list[FileStorage] = (await request.files).getlist("file")
    current_app.logger.info(files)
    image_type = filter(lambda x: "image" in x.content_type, files)
    try:
        file = next(image_type)
    except StopIteration:
        file = None

    if not file:
        await flash("Uploaded content is not an image!")
        return jsonify(image=None)

    filename = file.filename
    if not filename:
        await flash("No file part!")
        return jsonify(image=None)

    if not file or not is_image(filename):
        await flash("Could not recognize uploaded file as an image!")
        return jsonify(image=None)

    # read image file string data
    image_data = file.read()
    image = string_data_to_image(image_data)
    _, image_with_frame = cv2.imencode(".jpg", add_frame(image))

    return jsonify(image=as_url(as_b64(image_with_frame)))


@bp.route("/", methods=["GET"])
async def home_route() -> typing.Union[str, Response]:
    return await render_template("index.html")
