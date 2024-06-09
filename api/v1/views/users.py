#!/usr/bin/python3
"""Contains REST endpoints for User objects"""

from api.v1.views import app_views
from flask import abort, request, Response
from models import storage
from models.user import User


@app_views.get("/users", strict_slashes=False)
def all_users():
    """Returns all User objects"""
    users = [u.to_dict() for u in storage.all(User).values()]

    return users


@app_views.get("/users/<user_id>", strict_slashes=False)
def single_user(user_id):
    """Returns a single user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return user.to_dict()


@app_views.post("/users/", strict_slashes=False)
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
    user.save()

    return user.to_dict(), 201


@app_views.put("/users/<user_id>", strict_slashes=False)
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

    return user.to_dict(), 200


@app_views.delete("/users/<user_id>", strict_slashes=False)
def delete_user(user_id):
    """Deletes a single user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return {}, 200
