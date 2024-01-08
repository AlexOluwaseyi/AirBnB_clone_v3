#!/usr/bin/python3
""" A view for Amenity objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import abort, request, jsonify


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects:
    GET /api/v1/amenities
    """
    all_amenities = storage.all(Amenity)
    amenities_list = []
    for amenity in all_amenities.values():
        amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list), 200


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity_dict = amenity.to_dict()
    return jsonify(amenity_dict), 200


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>
    """
    amenity_to_delete = storage.get(Amenity, amenity_id)
    if amenity_to_delete is None:
        abort(404)

    storage.delete(amenity_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    Creates a Amenity: POST /api/v1/amenities
    """
    response = request.get_json()
    if response is None:
        abort(400, description="Not a JSON")

    if 'name' not in response:
        abort(400, description="Missing name")

    new_amenity = Amenity(**response)
    new_amenity.save()
    new_amenity_dict = new_amenity.to_dict()
    return jsonify(new_amenity_dict), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>
    """
    attr_list = ['id', 'created_at', 'updated_at']

    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    response = request.get_json()
    if response is None:
        abort(400, description="Not a JSON")

    for key, data in response.items():
        if key not in attr_list:
            setattr(state, key, data)
    amenity.save()
    amenity_dict = amenity.to_dict()
    return jsonify(amenity_dict), 200
