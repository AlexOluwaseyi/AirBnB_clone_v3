#!/usr/bin/python3
"""
Index route of the api
  - /status: returns a JSON {status: OK}
"""
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """ Returns a JSON {status:OK} """
    status = {'status': 'OK'}
    return (status)


@app_views.route("/stats", strict_slashes=False)
def stats():
    """ Endpoint that retrieves the number of each objects by type """
    object_counts = {}
    object_counts["amenities"] = storage.count(Amenity)
    object_counts["cities"] = storage.count(City)
    object_counts["places"] = storage.count(Place)
    object_counts["reviews"] = storage.count(Review)
    object_counts["states"] = storage.count(State)
    object_counts["users"] = storage.count(User)
    return (object_counts)
