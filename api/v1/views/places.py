#!/usr/bin/python3
"""
API routes for places
"""
from models import storage
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def places_all(city_id):
    """
    Retrieves the list of all Place objects of a City
       Parameters:
           city_id (str):
       Returns:
           A list of JSON dictionaries of all places in a city
    """
    city = storage.get(City, city_id)
    places_list = []
    if city:
        for place in city.places:
            places_list.append(place.to_dict())
        return jsonify(places_list)
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object.
       Parameters:
           place_id (str): place uuid
       Returns:
           JSON dictionary of place
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
    """
    Deletes a Place object.
       Parameters:
           place_id (str): place uuid
       Returns:
           Empty JSON dictionary if successful otherwise 404 error
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place.
       Parameters:
           city_id (str): city uuid
       Returns:
           JSON dictionary of place if successful
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        return make_response(jsonify('Not a JSON'), 400)
    if 'user_id' not in request.json:
        return make_response(jsonify('Missing user_id'), 400)
    user_id = request.json.get('user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' not in request.json:
        return make_response(jsonify('Missing name'), 400)
    content = request.get_json(silent=True)
    place = Place(**content)
    place.save()
    setattr(place, 'city_id', city_id)
    return make_response(place.to_json(), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """ handles PUT method """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    place = place.to_json()
    return make_response(jsonify(place), 200)
