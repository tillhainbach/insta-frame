"""Bootstrap Flask app instance."""

import os
from typing import Any, Mapping, Optional

from quart import Quart


def create_app(test_config: Optional[Mapping[str, Any]] = None) -> Quart:
    app = Quart(__name__, instance_relative_config=True)

    secret_key = os.environ["SECRET_KEY"]

    app.config.from_mapping(SECRET_KEY=secret_key)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)

    else:
        app.config.from_mapping(test_config)

    # ensure instance folder exists
    try:
        if app.instance_path is not None:
            os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import home

    app.register_blueprint(home.bp)
    app.add_url_rule("/", endpoint="index")

    return app
