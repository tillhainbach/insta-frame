"""Home View."""

import typing

from quart import Blueprint, current_app, flash, jsonify, render_template, request
from quart.wrappers.response import Response
from werkzeug.datastructures import FileStorage

from insta_frame.lib import is_image, upload_image_pipe

bp = Blueprint("home", __name__)


@bp.route("/?", methods=["POST"])
async def upload_image() -> Response:
    files: list[FileStorage] = (await request.files).getlist("file")
    current_app.logger.debug(files)
    image_type = filter(lambda x: "image" in x.content_type, files)

    try:
        file = next(image_type)
    except StopIteration:
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
    response_image = upload_image_pipe(file.read())

    return jsonify(image=response_image)


@bp.route("/", methods=["GET"])
async def home_route() -> typing.Union[str, Response]:
    return await render_template("index.html")
