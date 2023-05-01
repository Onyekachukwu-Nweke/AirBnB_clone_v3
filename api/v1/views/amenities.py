#!/usr/bin/python3
"""Routes for amenities module"""
from api.v1.views import app_views
from api.v1.views import *
from models import storage
from models.amenity import Amenity
from flask import jsonify, make_response, abort, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenities(amenity_id=None):
    """
    Retrieves all amenity or if an amenity id
    is specified it retrieves only that amenity
    """
    if not amenity_id:
        amenities = [amenity.to_dict() for amenity in
                     storage.all(Amenity).values()]
        return jsonify(amenities)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenities(amenity_id):
    """Deletes an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an amenity"""
    if request.json is None:
        return make_response(jsonify('Not a JSON'), 400)
    elif 'name' not in request.json:
        return make_response(jsonify('Missing name'), 400)
    content = request.get_json(silent=True)
    amenity = Amenity(**content)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    elif request.json is None:
        return make_response(jsonify('Not a JSON'), 400)
    for key, value in request.json().items():
        setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
