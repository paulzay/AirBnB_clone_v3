#!/usr/bin/python3
"""routing"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status_route():
    """return status OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats_route():
    """Returns the number of objects by type"""

    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User,
    }

    obj_stats = {k: storage.count(v) for k, v in classes.items()}

    return obj_stats
