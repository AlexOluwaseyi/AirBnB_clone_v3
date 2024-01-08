#!/usr/bin/python3
"""
Index route of the api
  - /status: returns a JSON {status: OK}
"""
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    """ Returns a JSON {status:OK} """
    status = {'status': 'OK'}
    return (status)
