#!/usr/bin/python3
"""Contains REST endpoints for City objects"""

from api.v1.views import app_views
from flask import abort, request, Response
from models import storage
from models.state import State
from models.city import City


@app_views.get("/states/<state_id>/cities", strict_slashes=False)
def all_state_cities(state_id):
    """Returns all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [c.to_dict() for c in state.cities]

    return cities


@app_views.get("/cities/<city_id>", strict_slashes=False)
def single_city(city_id):
    """Returns a single City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return city.to_dict()


@app_views.post("/states/<state_id>/cities", strict_slashes=False)
def create_city(state_id):
    """Creates a City object"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    city_dict = request.get_json(silent=True)
    if not city_dict:
        abort(Response("Not a JSON", 400))

    if "name" not in city_dict:
        abort(Response("Missing name", 400))

    city = City(**city_dict)
    city.state_id = state_id
    storage.new(city)
    storage.save()

    return city.to_dict(), 201


@app_views.put("/cities/<city_id>", strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    city_dict = request.get_json(silent=True)
    if not city_dict:
        abort(Response("Not a JSON", 400))

    ignore = ["id", "state_id", "created_at", "updated_at"]
    for attr, val in city_dict.items():
        if attr not in ignore:
            setattr(city, attr, val)
    storage.save()

    return city.to_dict(), 200


@app_views.delete("/cities/<city_id>", strict_slashes=False)
def delete_city(city_id):
    """Deletes a single city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return {}, 200
