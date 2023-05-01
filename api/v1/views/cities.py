#!/usr/bin/python3

"""All REASTFUL API for STATES"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.state import State
from models.city import City
from models import storage


@app_views.route("/states/<state_id>/cities")
def cities_methods(state_id):
    return jsonify({})
