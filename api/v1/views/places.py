#!/usr/bin/python3
""" A view for Place objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from flask import abort, request, jsonify


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City:
    GET /api/v1/cities/<city_id>/places
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    places_list = [place.to_dict() for place in places]
    return jsonify(places_list), 200


@app_views.route("/places/<place_id>",
                 methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object. : GET /api/v1/places/<place_id>
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object: DELETE /api/v1/places/<place_id>
    """
    place_to_delete = storage.get(Place, place_id)
    if place_to_delete is None:
        abort(404)

    storage.delete(place_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place: POST /api/v1/cities/<city_id>/places
    """
    response = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if response is None:
        abort(400, description="Not a JSON")

    if 'user_id' not in response:
        abort(400, description="Missing user_id")

    user_id = response.get("user_id")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if 'name' not in response:
        abort(400, description="Missing name")

    response["city_id"] = city_id
    place = Place(**response)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>",
                 methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object: PUT /api/v1/places/<place_id>
    """
    attr_list = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    response = request.get_json()
    if response is None:
        abort(400, description="Not a JSON")

    for key, data in response.items():
        if key not in attr_list:
            setattr(place, key, data)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search/", methods=['POST'], strict_slashes=False)
def places_search():
    """ Retrieves all Place objects depending on the JSON in the request body.
    JSON can contain 3 optional keys:
    - states: list of State ids
    - cities: list of City ids
    - amenities: list of Amenity ids
    """

    data = request.get_json()

    # Checks if data is JSON
    if not data:
        abort(400, 'Not a JSON')

    states_ids = data.get("states", [])
    cities_ids = data.get("cities", [])
    amenities_ids = data.get("amenities", [])

    places = []

    # Checks if JSON keys has states, cities and/or amenities
    # Retrieves all places if not
    if not states_ids and not cities_ids and not amenities_ids:
        places = storage.all(Place).values()

    else:
        # Retrieve places based on states
        for state_id in states_ids:
            state = storage.get(State, state_id)
            if state:
                places.extend(state.cities)

        # Retrieve places based on cities
        for city_id in cities_ids:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)

    # Filter places based on amenities
    if amenities_ids:
        amenities = [storage.get(Amenity, amenity_id)
                     for amenity_id in amenities_ids]
        places = [place for place in places if all(
                  amenity in place.amenities for amenity in amenities
                  )]

    places_list = [place.to_dict() for place in set(places)]

    return jsonify(places_list), 200
