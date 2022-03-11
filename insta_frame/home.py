"""Home View."""

import typing

import cv2
from flask import (
    Blueprint,
    current_app,
    jsonify,
    make_response,
    render_template,
    request,
)
from werkzeug.wrappers.response import Response

from insta_frame.lib import add_frame, as_b64, as_url, is_image, string_data_to_image

bp = Blueprint("home", __name__)


@bp.route("/?", methods=["POST"])
def upload_image() -> Response:
    files = request.files.getlist("file")
    image_type = filter(lambda x: "image" in x.content_type, files)
    file = next(image_type)
    current_app.logger.info(request.files)
    if not file:
        return jsonify(success=False, error="No data was uploaded!")

    filename = file.filename
    if not filename:
        return make_response("No file part!", 400)

    if not file or not is_image(filename):
        return make_response("No image selected!", 400)

    # read image file string data
    image_data = file.read()
    image = string_data_to_image(image_data)
    _, image_with_frame = cv2.imencode(".jpg", add_frame(image))

    return jsonify(image=as_url(as_b64(image_with_frame)))


@bp.route("/", methods=["GET"])
def home_route() -> typing.Union[str, Response]:
    return render_template("index.html")
