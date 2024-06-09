#!/usr/bin/python3
"""Contains REST endpoints for Amenities objects"""

from api.v1.views import app_views
from flask import abort, request, Response
from models import storage
from models.amenity import Amenity


@app_views.get("/amenities", strict_slashes=False)
def all_amenities():
    """Returns all Amenity objects"""
    amenities = [obj.to_dict() for obj in storage.all(Amenity).values()]

    return amenities


@app_views.get("/amenities/<amenity_id>", strict_slashes=False)
def single_amenity(amenity_id):
    """Returns a single amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    return amenity.to_dict()


@app_views.post("/amenities/", strict_slashes=False)
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


@app_views.put("/amenities/<amenity_id>", strict_slashes=False)
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


@app_views.delete("/amenities/<amenity_id>", strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return {}, 200
