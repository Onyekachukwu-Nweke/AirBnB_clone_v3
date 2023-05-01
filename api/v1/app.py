#!/usr/bin/python3

"""A Script that imports a blueprint and Flask"""

from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def clean_up(execption=None):
    """eliminates current Session"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """handles an error of 404"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    app.run(host, int(port), threaded=True)
