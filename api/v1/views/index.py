#!/usr/bin/python3
"""routing"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status_route():
    """return status OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats_route():
    """Returns the number of objects by type"""

    obj_dict = storage.all()
    obj_stats = {}
    for obj_id in obj_dict:
        cls = obj_id.split(".")[0].lower()
        obj_stats[cls] = obj_stats.setdefault(cls, 0) + 1

    return obj_stats
