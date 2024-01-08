#!/usr/bin/python3
""" A view for State objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import abort, request, jsonify


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects:
        GET /api/v1/states
    """
    all_states = storage.all(State)
    states_list = []
    for state in all_states.values():
        states_list.append(state.to_dict())
    return (states_list, 200)


@app_views.route("/states/<string:state_id>", methods=["GET"],
                 strict_slashes=False)
def get_state(state_id=None):
    """
    Retrieves a State object:
        GET /api/v1/states/<state_id>
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_dict = state.to_dict()
    return (state_dict, 200)


@app_views.route("/states/<string:state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_states(state_id=None):
    """
    Deletes a State object:
        DELETE /api/v1/states/<state_id>
    """
    state_to_delete = storage.get(State, state_id)
    if state_to_delete is None:
        abort(404)
    storage.delete(state_to_delete)
    storage.save()
    return ({}, 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """ Add new State """
    response = request.get_json()
    if response is None:
        abort(400, description="Not a JSON")

    if 'name' not in response:
        abort(400, description="Missing name")

    new_state = State(**response)
    new_state.save()
    new_state_dict = new_state.to_dict()
    return (new_state_dict, 201)


@app_views.route("/states/<string:state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """ Updates a State object """
    attr_list = ['id', 'created_at', 'updated_at']

    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    response = request.get_json()
    if response is None:
        abort(400, description="Not a JSON")

    for key, data in response.items():
        if key not in attr_list:
            setattr(state, key, data)
    state.save()
    state_dict = state.to_dict()
    return (state_dict, 200)
