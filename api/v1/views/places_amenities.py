#!/usr/bin/python3
"""Contains REST endpoints for Amenities objects"""

from api.v1.views import app_views
from flask import abort
from models import storage
from models.amenity import Amenity
from models.place import Place
from models import storage_t


@app_views.get("/places/<place_id>/amenities", strict_slashes=False)
def get_amenities(place_id):
    """Returns all Amenity objects"""
    if storage_t == "db":
        place = storage.get(Place, place_id)
        if not place:
            abort(404)

        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [amenity.to_dict()
                     for amenity in storage.all(Amenity).values()]

    return amenities


@app_views.delete("/places/<place_id>/amenities/<amenity_id>",
                  strict_slashes=False)
def delete_amenity_to_place(amenity_id, place_id):
    """Deletes an Amenity object from a Place object"""
    if storage_t == "db":
        place = storage.get(Place, place_id)
        if not place:
            abort(404)

        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)

        if amenity not in place.amenities:
            abort(404)

        place.amenities.remove(amenity)
        storage.save()
    else:
        place = storage.get(Place, place_id)
        if not place:
            abort(404)

        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)

        if amenity not in place.amenities:
            abort(404)

        place.amenities.remove(amenity)
        storage.save()

    return {}, 200


@app_views.post("/places/<place_id>/amenities/<amenity_id>",
                strict_slashes=False)
def link_amenity(amenity_id, place_id):
    """Links an Amenity object to a Place object"""
    if storage_t == "db":
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)

        place = storage.get(Place, place_id)
        if not place:
            abort(404)

        if amenity in place.amenities:
            return amenity.to_dict(), 200

        place.amenities.append(amenity)
        storage.save()
    else:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)

        place = storage.get(Place, place_id)
        if not place:
            abort(404)

        if amenity in place.amenities:
            return amenity.to_dict(), 200

        place.amenities.append(amenity)
        storage.save()

    return amenity.to_dict(), 201
