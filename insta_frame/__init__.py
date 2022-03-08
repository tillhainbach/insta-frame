"""Bootstrap Flask app instance."""

import os
import shutil
import tempfile
from functools import partial
from typing import Any, Mapping, Optional

from flask import Flask, appcontext_tearing_down


def clean_up_temp(temp: str, *args, **kwargs) -> None:
    shutil.rmtree(temp, ignore_errors=True)
    return


def create_app(test_config: Optional[Mapping[str, Any]] = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(SECRET_KEY="dev")

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)

    else:
        app.config.from_mapping(test_config)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    temp = tempfile.mkdtemp()
    app.config["UPLOAD_FOLDER"] = temp

    appcontext_tearing_down.connect(partial(clean_up_temp, temp))

    from . import home

    app.register_blueprint(home.bp)
    app.add_url_rule("/", endpoint="index")

    return app
