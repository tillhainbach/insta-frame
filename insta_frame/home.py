"""Home View."""

import os
import typing

import cv2
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename
from werkzeug.wrappers.response import Response

from insta_frame.lib import add_frame, is_image, string_data_to_image

bp = Blueprint("home", __name__)


@bp.route("/<name>")
def download_file(name) -> Response:
    temp = current_app.config["UPLOAD_FOLDER"]
    current_app.logger.info(f"Storing files to: {temp}")

    return send_from_directory(temp, name)


@bp.route("/", methods=["GET", "POST"])
def home_route() -> typing.Union[str, Response]:
    name = "file"

    if request.method == "POST":
        # check if the post request has the file part
        if name not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files[name]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        filename = file.filename
        if filename is None or filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and is_image(filename):
            flash("Received file!")
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
