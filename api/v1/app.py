#!/usr/bin/python3
"""Starts a Flask web application
"""

from api.v1.views import app_views
from flask import Flask
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """call storage.close"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """handle 404 errors"""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", "5000"))
    app.run(host, port, threaded=True)
