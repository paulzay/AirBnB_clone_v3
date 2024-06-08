#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """call storage.close"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", "5000"))
    app.run(host, port, threaded=True)
