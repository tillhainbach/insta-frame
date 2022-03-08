# from .__init__ import create_app

from flask import Flask

# application = create_app()

application = Flask(__name__)
application.secret_key = "super_secret!"


@application.route("/")
def hello_world():
    return "Hello World!"
