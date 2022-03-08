# from .__init__ import create_app

import shutil
import tempfile

from flask import Flask, appcontext_tearing_down

# application = create_app()

application = Flask(__name__)
application.secret_key = "super_secret!"

temp = tempfile.mkdtemp()
application.config["UPLOAD_FOLDER"] = temp


def _cleanup(*args, **kwargs):
    shutil.rmtree(temp)
    return


appcontext_tearing_down.connect(_cleanup)


@application.route("/")
def hello_world():
    return "Hello World!"
