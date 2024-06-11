#!/usr/bin/python3
"""Contains REST endpoints for Amenity objects"""

from api.v1.views import app_views
from flask import abort, request, Response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'])
def all_amenities():
    """Returns all Amenity objects"""
    amenities = [obj.to_dict() for obj in storage.all(Amenity).values()]

    return amenities


@app_views.route("/amenities/<amenity_id>", methods=['GET'])
def single_amenity(amenity_id):
    """Returns a single amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return amenity.to_dict()


@app_views.route("/amenities/", methods=['POST'])
def create_amenity():
    """Creates a Amenity object"""

    amenity_dict = request.get_json(silent=True)
    if not amenity_dict:
        abort(Response("Not a JSON", 400))

    if "name" not in amenity_dict:
        abort(Response("Missing name", 400))

    amenity = Amenity(**amenity_dict)
    storage.new(amenity)
    storage.save()

    return amenity.to_dict(), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a Amenity object"""

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    amenity_dict = request.get_json(silent=True)
    if not amenity_dict:
        abort(Response("Not a JSON", 400))

    ignore = ["id", "created_at", "updated_at"]
    for attr, val in amenity_dict.items():
        if attr not in ignore:
            setattr(amenity, attr, val)
    storage.save()

    return amenity.to_dict(), 200


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a single amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return {}, 200
