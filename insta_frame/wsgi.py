# from .__init__ import create_app

import shutil
import tempfile

from flask import Flask, appcontext_tearing_down

from . import home

# application = create_app()

application = Flask(__name__)
application.secret_key = "super_secret!"

temp = tempfile.mkdtemp()
application.config["UPLOAD_FOLDER"] = temp


def _cleanup(*args, **kwargs):
    shutil.rmtree(temp, ignore_errors=True)
    return


appcontext_tearing_down.connect(_cleanup)


application.register_blueprint(home.bp)
application.add_url_rule("/", endpoint="index")


# @application.route("/")
# def hello_world():
#     return "Hello World!"
