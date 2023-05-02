#!/usr/bin/python3
"""Routes for user module"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, make_response, abort, request


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """
    Gets the total number of users in list
    in 200 http response
    """
    all_users = [user.to_dict() for user in
                 storage.all(User).values()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """
    Shows a specific user based on id.
        Parameters:
            user_id [str]: the id of the user to display

        Returns:
            A JSON dictionary of the user in a 200 response
            A 404 response if the id does not match
    """
    user = storage.all(User, user_id)
    if not user:
        return (jsonify(user.to_dict()))
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """
    Deletes a specific user based on id.
        Parameters:
            user_id [str]: the id of the user to delete

        Returns:
            An empty JSON dictionary in a 200 response
            A 404 response if the id does not match
    """
    user = storage.all(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """
    Creates a new user.
        Returns:
            A JSON dictionary of a new user in a 200 response
            A 400 response if missing parameters or if not valid JSON
    """
    if request.json is None:
        return make_response(jsonify({"error": "Not found"}), 400)
    content = request.get_json(silent=True)
    if "email" in content.keys() and "password" in content.keys():
        user = User(**content)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)
    else:
        if "email" not in content.keys():
            return make_response(jsonify({'error': 'Missing email'}), 400)
        if "password" not in content.keys():
            return make_response(jsonify({'error': 'Missing password'}), 400)


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates an user using its user id
        Parameters:
            user_id [str]: the id of the user to update

        Returns:
            A JSON dictionary of the updated user in a 200 response
            A 400 response if not a valid JSON
            A 404 response if the id does not match
    """
    ignore = ['id', 'email', 'created_at', 'updated_at']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    elif request.json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    content = request.get_json(silent=True)
    for key, value in content.items():
        if key not in ignore:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
