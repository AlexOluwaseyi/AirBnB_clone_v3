#!/usr/bin/python3
""" A view for Review objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from flask import abort, request, jsonify


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place:
    GET /api/v1/places/<place_id>/reviews
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = place.reviews
    review_list = []
    for review in reviews:
        review_list.append(review.to_dict())
    return jsonify(review_list), 200


@app_views.route("/reviews/<review_id>",
                 methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object. : GET /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object: DELETE /api/v1/reviews/<review_id>
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review: POST /api/v1/places/<place_id>/reviews
    """
    response = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if response is None:
        abort(400, description="Not a JSON")

    if "user_id" not in response:
        abort(400, description="Missing user_id")

    user_id = response.get("user_id")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if "text" not in response:
        abort(400, description="Missing text")

    response["place_id"] = place_id
    new_review = Review(**response)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>",
                 methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object: PUT /api/v1/reviews/<review_id>
    """
    attr_list = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    response = request.get_json()
    if response is None:
        abort(400, description="Not a JSON")

    for key, data in response.items():
        if key not in attr_list:
            setattr(review, key, data)
    review.save()
    return jsonify(review.to_dict()), 200
