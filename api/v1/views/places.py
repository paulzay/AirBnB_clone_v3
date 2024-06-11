#!/usr/bin/python3
"""Contains REST endpoints for Place objects"""

from api.v1.views import app_views
from flask import abort, jsonify, request, Response
from models import storage, storage_t
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def all_places(city_id):
    """Returns all Place objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = []
    if storage_t == "db":
        places = [place.to_dict() for place in city.places]
    else:
        places = [
            place.to_dict()
            for place in storage.all(Place).values()
            if place.city_id == city_id
        ]

    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"])
def place(place_id):
    """Returns a single place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return place.to_dict()


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Deletes a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return {}, 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """Creates a Place object"""

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    place_dict = request.get_json(silent=True)
    if not place_dict:
        abort(Response("Not a JSON", 400))

    if "user_id" not in place_dict:
        abort(Response("Missing user_id", 400))

    user = storage.get(User, place_dict["user_id"])
    if not user:
        abort(404)

    if "name" not in place_dict:
        abort(Response("Missing name", 400))

    place = Place(**place_dict)
    place.city_id = city_id
    storage.new(place)
    storage.save()

    return place.to_dict(), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place_dict = request.get_json(silent=True)
    if not place_dict:
        abort(Response("Not a JSON", 400))

    ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for attr, val in place_dict.items():
        if attr not in ignore:
            setattr(place, attr, val)
    storage.save()

    return place.to_dict(), 200
