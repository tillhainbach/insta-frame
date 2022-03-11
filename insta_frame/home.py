"""Home View."""

import os
import typing

import cv2
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename
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


@bp.route("/<name>")
def download_file(name) -> Response:
    temp = current_app.config["UPLOAD_FOLDER"]
    current_app.logger.info(f"Storing files to: {temp}")

    return send_from_directory(temp, name)


@bp.route("/", methods=["GET", "POST"])
def home_route() -> typing.Union[str, Response]:

    if request.method == "POST":
        current_app.logger.info(request.files)

        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        filename = file.filename
        if not filename:
            flash("No file selected")
            return redirect(request.url)

        if file and is_image(filename):
            # read image file string data
            image_data = file.read()
            image = string_data_to_image(image_data)
            image_with_frame = add_frame(image)
            filename = secure_filename(filename)
            cv2.imwrite(
                os.path.join(current_app.config["UPLOAD_FOLDER"], filename),
                image_with_frame,
            )
            return redirect(url_for("home.download_file", name=filename))

        return redirect(request.url)

    return render_template("index.html")
