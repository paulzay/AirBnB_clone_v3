#!/usr/bin/python3
"""routing"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status_route():
    """return status OK"""
    return jsonify({"status": "OK"})
