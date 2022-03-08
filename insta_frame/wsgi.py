import logging

from .__init__ import create_app

application = create_app()

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    application.logger.handlers = gunicorn_logger.handlers
    application.logger.setLevel(gunicorn_logger.level)

# if "DYNO" in os.environ:
#     application.logger.addHandler(logging.StreamHandler(sys.stdout))
#     application.logger.setLevel(logging.ERROR)
