#!/usr/bin/python3
"""
This sets up the app for the api of the project
"""
from flask import Flask
from os import getenv
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def remove_session(exception):
    """ Ends a session """
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST") or '0.0.0.0',
            port=getenv("HBNB_API_PORT") or 5000,
            threaded=True)
