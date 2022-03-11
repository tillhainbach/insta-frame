import logging

from .__init__ import create_app

app = create_app()

if __name__ != "__main__":
    hypercorn = logging.getLogger("hypercorn.error")
    app.logger.handlers = hypercorn.handlers
    app.logger.setLevel(hypercorn.level)
