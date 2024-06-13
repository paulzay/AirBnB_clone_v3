#!/usr/bin/python3
"""Contains REST endpoints for User objects"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"])
def all_users():
    """Returns all User objects"""
    users = [u.to_dict() for u in storage.all(User).values()]

    return jsonify(users)


@app_views.route("/users/<user_id>", methods=["GET"])
def single_user(user_id):
    """Returns a single user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/", methods=["POST"])
def create_user():
    """Creates a User object"""
    user_dict = request.get_json(silent=True)
    if not user_dict:
        abort(Response("Not a JSON", 400))

    if "email" not in user_dict:
        abort(Response("Missing email", 400))

    if "password" not in user_dict:
        abort(Response("Missing password", 400))

    user = User(**user_dict)
    storage.new(user)
    storage.save()

    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Updates a User object"""

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user_dict = request.get_json(silent=True)
    if not user_dict:
        abort(Response("Not a JSON", 400))

    ignore = ["id", "email", "created_at", "updated_at"]
    for attr, val in user_dict.items():
        if attr not in ignore:
            setattr(user, attr, val)
    storage.save()

    return make_response(jsonify(user.to_dict()), 200)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Deletes a single user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)
