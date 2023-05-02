#!/usr/bin/python3
"""
API routes for places review
"""
from models import storage
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews/',
                 methods=['GET'], strict_slashes=False)
def all_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place.
        Parameters:
            place_id [str]: the id of the place to display reviews of
        Returns:
            A list of JSON dictionaries of all reviews in a 200 response
    """
    reviews_list = []
    place = storage.get(Place, place_id)
    if place:
        for review in place.reviews:
            reviews_list.append(review.to_dict())
        return jsonify(reviews_list)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>/',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object.
        Parameters:
            review_id [str]: the id of the review to display
        Returns:
            A JSON dictionary of the review in a 200 response
            A 404 response if the id does not match
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews/',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review.
        Parameters:
            place_id [str]: the id of the place to add the review to
        Returns:
            A JSON dictionary of a new review in a 200 response
            A 400 response if missing parameters or if not valid JSON
    """
    error_message = ""
    place = storage.get(Place, place_id)
    if place:
        content = request.get_json(silent=True)
        if type(content) is dict:
            if "user_id" not in content.keys():
                error_message = "Missing user_id"
            elif "text" not in content.keys():
                error_message = "Missing text"
            else:
                user = storage.get(User, content['user_id'])
                if user:
                    review = Review(**content)
                    review.place_id = place_id
                    storage.new(review)
                    storage.save()
                    return make_response(jsonify(review.to_dict()), 201)

                else:
                    abort(404)
        else:
            error_message = "Not a JSON"
        return make_response(jsonify({"error": error_message}), 400)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>/', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review object
    Parameters:
        review_id [str]: the id of the review to update
    Returns:
        A JSON dictionary of the updated review in a 200 response
        A 400 response if not a valid JSON
        A 404 response if the id does not match
    """
    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    review = storage.get(Review, review_id)
    if review:
        content = request.get_json(silent=True)
        if type(content) is dict:
            for key, value in content.items():
                if key not in ignore:
                    setattr(review, key, value)
            storage.save()
            return jsonify(review.to_dict())

        else:
             return make_response(jsonify({"error": "Not a JSON"}), 400)
    else:
        abort(404)
