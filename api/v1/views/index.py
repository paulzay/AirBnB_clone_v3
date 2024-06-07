#!/usr/bin/python3
"""docs"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status_route():
  """return status OK"""
  return jsonify({'status': 'OK'})
