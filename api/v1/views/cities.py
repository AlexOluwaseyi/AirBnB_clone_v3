#!/usr/bin/python3

"""
Creates new view for City objects that handles all default RESTFul API actions
Retrieves the list of all City objects of a State:
GET /api/v1/states/<state_id>/cities
Retrieves a City object. : GET /api/v1/cities/<city_id>
Deletes a City object: DELETE /api/v1/cities/<city_id>
Creates a City: POST /api/v1/states/<state_id>/cities
Updates a City object: PUT /api/v1/cities/<city_id>
"""

from flask import Flask, jsonify, abort, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views

app = Flask(__name__)


@app_views.route("/states/<state_id>/cities/", methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """ Get list of cities in state by state_id"""
    # Use the get method to get states based on state_id
    state = storage.get(State, state_id)

    # If state not found (or incorrect ID)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=['GET'],
                 strict_slashes=False)
def get_cities_by_id(city_id):
    """Gets a city by City id"""
    # Get city with get method in storage
    city = storage.get(City, city_id)

    # If city not found by city_id
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """Deletes a City object by City id"""
    # Get city objects with get method
    city = storage.get(City, city_id)

    # If city not found by city_id
    if not city:
        abort(404)

    # Delete using storage.delete() method and return empty dict and save
    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities/", methods=['POST'],
                 strict_slashes=False)
def create_city_in_state(state_id):
    """Creates a city in a state bu state id"""
    # Get state object by id using storeage.get() method
    state = storage.get(State, state_id)

    # Check if state is found by state_id
    if not state:
        abort(404)

    data = request.get_json()

    # Checks data if it is a JSON and has 'name' as a key
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')

    # Unpack and create new city in state with state_id
    new_city = City(**data)
    new_city.state_id = state.id

    # Save the new City to the storage
    storage.new(new_city)
    storage.save()

    # Return the new City with the status code 201
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200
