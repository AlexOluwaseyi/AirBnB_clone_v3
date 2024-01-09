#!/usr/bin/python3
""" A view for Place and Amenity objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from models import storage, storage_t
from flask import abort, request, jsonify


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"], strict_slashes=False)
def get_amenities_of_a_place(place_id):
    """
    Retrieves the list of all Amenity objects of a Place:
    GET /api/v1/places/<place_id>/amenities
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if storage_t == "db":
        amenities = place.amenities
        amenities_list = [amenity.to_dict() for amenity in amenities]
        return jsonify(amenities_list), 200
    else:
        amenities_id = place.amenity_ids
        return jsonify(amenities_id), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def remove_amenity_from_place(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place:
    DELETE /api/v1/places/<place_id>/amenities/<amenity_id>
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if storage_t == "db":
        for linked_amenity in place.amenities:
            if linked_amenity.id == amenity.id:
                place.amenities.remove(amenity)
                place.save()
                storage.save()
                return jsonify({}), 200
        abort(404)
    else:
        for a_id in place.amenity_ids:
            if a_id == amenity_id:
                place.amenity_ids.remove(a_id)
                return jsonify({}), 200
        abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def link_amenity_to_place():
    """
    Link a Amenity object to a Place:
    POST /api/v1/places/<place_id>/amenities/<amenity_id>
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if storage_t == "db":
        for linked_amenity in place.amenities:
            if linked_amenity.id == amenity.id:
                return jsonify(amenity.to_dict()), 201
        place.amenities.append(amenity)
        return jsonify(amenity.to_dict()), 201
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 201
        place.amenity_ids.append(amenity_id)
        return jsonify(amenity.to_dict()), 201
