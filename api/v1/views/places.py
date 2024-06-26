#!/usr/bin/python3
"""Contains REST endpoints for Place objects"""

from api.v1.views import app_views
from flask import abort, jsonify, request, Response, make_response
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

    places = [place.to_dict() for place in city.places]

    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"])
def place(place_id):
    """Returns a single place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Deletes a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


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

    return make_response(jsonify(place.to_dict()), 201)


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

    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
