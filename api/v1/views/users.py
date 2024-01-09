#!/usr/bin/python3

"""
Creates new view for Users objects that handles all default RESTFul API actions
Retrieves the list of all User objects: GET /api/v1/views/
Retrieves a User object: GET /api/v1/users/<user_id>
Deletes a User object:: DELETE /api/v1/users/<user_id>
Creates a User: POST /api/v1/users


"""

from flask import Flask, jsonify, abort, request
from models.user import User
from models import storage
from api.v1.views import app_views

app = Flask(__name__)


@app_views.route("/users/", methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """ Get list of user in User object"""
    # Use the get method to get states based on state_id
    users = storage.all(user)

    # If state not found (or incorrect ID)
    if users is None:
        abort(404)

    allUser = [eachUser.to_dict() for eachUser in users]
    return jsonify(allUser)


@app_views.route("/users/<user_id>/", methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object based on user_id)"""
    # Use the get method to get user with user_id
    user = storage.get(User, user_id)

    # Checks user object (or its user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>/", methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """Deletes a User object"""
    # Use the get method to get the user with user_id
    user = storage.get(User, user_id)

    # Check user is found (or incorrect user_id
    if not user:
        abort(404)

    # Delete and save changes to storgae
    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route("/users/", methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User and returns the user with a status code of 201"""
    # Get data for new user
    data = request.get_json()

    # Check if data is JSON and if other keys are present
    if not data:
        abort(400, 'Not a JSON')

    if 'email' not in data.keys():
        abort(400, 'Missing eail')
    if 'password' not in data.keys():
        abort(400, 'Missing password')

    # Create a new user from the User model
    new_user = User(**data)

    # Creates and save the new user to storage
    storage.new(new_user)
    storage.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object bu usaer_id"""
    # Use the get method ot get user
    user = storage.get(User, user_id)

    # Checks the user
    if not user:
        abort(404)

    data = request.get_json()

    # Checked if the data meets recovery
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
