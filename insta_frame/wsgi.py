import logging
import os
import sys

from .__init__ import create_app

application = create_app()


if "DYNO" in os.environ:
    application.logger.addHandler(logging.StreamHandler(sys.stdout))
    application.logger.setLevel(logging.ERROR)
