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
    try:
        state = storage.get(State, state_id)
        return (state.to_dict(), 200)
    except Exception:
        abort(404)


@app_views.route("/states/<string:state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_states(state_id=None):
    """
    Deletes a State object:
        DELETE /api/v1/states/<state_id>
    """
    if state_id is None:
        abort(404)

    try:
        state = storage.get(State, state_id)
        state.delete()
        storage.save()
        return ({}, 200)
    except Exception:
        abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """ Add new State """
    try:
        response = request.get_json()
        if 'name' not in response:
            abort(400, description="Missing name")

        new_state = State()
        new_state.name = response.get('name')
        new_state.save()
        return (new_state.to_dict(), 201)
    except Exception:
        abort(400, description="Not a JSON")


@app_views.route("/states/<string:state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """ Updates a State object """
    attr_list = ['id', 'created_at', 'updated_at']

    if state_id is None:
        abort(404)

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    try:
        response = request.get_json()
        for key, data in response.items():
            if key not in attr_list:
                setattr(state, key, data)
        state.save()
        return (state.to_dict(), 200)
    except Exception:
        abort(400, description="Not a JSON")
