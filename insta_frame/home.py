"""Home View."""

import typing

import cv2
from flask import Blueprint, flash, jsonify, render_template, request
from werkzeug.wrappers.response import Response

from insta_frame.lib import add_frame, as_b64, as_url, is_image, string_data_to_image

bp = Blueprint("home", __name__)


@bp.route("/?", methods=["POST"])
def upload_image() -> Response:
    files = request.files.getlist("file")
    image_type = filter(lambda x: "image" in x.content_type, files)
    try:
        file = next(image_type)
    except StopIteration:
        file = None

    if not file:
        flash("Uploaded content is not an image!")
        return jsonify(image=None)

    filename = file.filename
    if not filename:
        flash("No file part!")
        return jsonify(image=None)

    if not file or not is_image(filename):
        flash("Could not recognize uploaded file as an image!")
        return jsonify(image=None)

    # read image file string data
    image_data = file.read()
    image = string_data_to_image(image_data)
    _, image_with_frame = cv2.imencode(".jpg", add_frame(image))

    return jsonify(image=as_url(as_b64(image_with_frame)))


@bp.route("/", methods=["GET"])
def home_route() -> typing.Union[str, Response]:
    return render_template("index.html")
