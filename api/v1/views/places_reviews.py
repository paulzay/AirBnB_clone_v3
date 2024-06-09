#!/usr/bin/python3
"""Contains REST endpoints for Place Review objects"""

from api.v1.views import app_views
from flask import abort, request, Response
from models import storage
from models.place import Place
from models.review import Review


@app_views.get("/places/<place_id>/reviews", strict_slashes=False)
def all_reviews(place_id):
    """Returns all Review objects"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]

    return reviews

@app_views.get("/reviews/<review_id>", strict_slashes=False)
def review(review_id):
    """Returns a single review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return review.to_dict()

@app_views.delete("/reviews/<review_id>", strict_slashes=False)
def delete_review(review_id):
    """Deletes a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return {}, 200

@app_views.post("/places/<place_id>/reviews", strict_slashes=False)
def create_review(place_id):
    """Creates a Review object"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    review_dict = request.get_json(silent=True)
    if not review_dict:
        abort(Response("Not a JSON", 400))

    if "user_id" not in review_dict:
        abort(Response("Missing user_id", 400))

    if "text" not in review_dict:
        abort(Response("Missing text", 400))

    review = Review(**review_dict)
    review.place_id = place_id
    storage.new(review)
    storage.save()

    return review.to_dict(), 201

@app_views.put("/reviews/<review_id>", strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""

    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    review_dict = request.get_json(silent=True)
    if not review_dict:
        abort(Response("Not a JSON", 400))

    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for attr, val in review_dict.items():
        if attr not in ignore:
            setattr(review, attr, val)
    storage.save()

    return review.to_dict(), 200
