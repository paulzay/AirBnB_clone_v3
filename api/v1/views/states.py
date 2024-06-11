#!/usr/bin/python3
"""Contains REST endpoints for State objects"""

from api.v1.views import app_views
from flask import abort, request, Response
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"])
def all_states():
    """Returns all State objects"""
    states = [st.to_dict() for st in storage.all(State).values()]

    return states


@app_views.route("/states/<state_id>", methods=["GET"])
def single_state(state_id):
    """Returns a single state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return state.to_dict()


@app_views.route("/states/", methods=["POST"])
def create_state():
    """Creates a State object"""

    state_dict = request.get_json(silent=True)
    if not state_dict:
        abort(Response("Not a JSON", 400))

    if "name" not in state_dict:
        abort(Response("Missing name", 400))

    state = State(**state_dict)
    storage.new(state)
    storage.save()

    return state.to_dict(), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """Updates a State object"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    state_dict = request.get_json(silent=True)
    if not state_dict:
        abort(Response("Not a JSON", 400))

    ignore = ["id", "created_at", "updated_at"]
    for attr, val in state_dict.items():
        if attr not in ignore:
            setattr(state, attr, val)
    storage.save()

    return state.to_dict(), 200


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Deletes a single state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return {}, 200
