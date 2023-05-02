#!/usr/bin/python3

"""Routes for amenities module"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import request, jsonify, abort


@app_views.route('/amenities',
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenities(amenity_id=None):
    """
    Retrieves all amenity or if an amenity id
    is specified it retrieves only that amenity
    """
    amenity_objs = storage.all(Amenity)

    amenities = [obj.to_dict() for obj in amenity_objs.values()]
    if not amenity_id:
        if request.method == 'POST':
            my_dict = request.get_json()

            if my_dict is None:
                abort(400, 'Not a JSON')
            if my_dict.get("name") is None:
                abort(400, 'Missing name')
            new_amenity = Amenity(**my_dict)
            new amenity.save()
            return jsonify(new_amenity.to_dict()), 201
          else:
        if request.method == 'GET':
            for amenity in amenities:
                if amenity.get('id') == amenity_id:
                    return jsonify(amenity)
            abort(404)
        elif request.method == 'PUT':
            my_dict = request.get_json()
            if my_dict is None:
                abort(400, 'Not a JSON')
            for amenity in amenity_objs.values():
                if amenity.id == amenity_id:
                    amenity.name = my_dict.get("name")
                    amenity.save()
                    return jsonify(amenity.to_dict()), 200
            abort(404)
        elif request.method == 'DELETE':
            for obj in amenity_objs.values():
                if obj.id == amenity_id:
                    storage.delete(obj)
                    storage.save()
                    return jsonify({}), 200
            abort(404)
            
