#!/usr/bin/python3
"""Reviews object view"""
from flask import Flask, jsonify, request, Response
from flask import abort
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def reviews(place_id):
    """Retrieve all reviews of place using place_id"""
    review_list = []

    if place_id is not None:
        all_reviews = storage.all(Review)

        single_place = storage.get(Place, place_id)

        if single_place is None:
            abort(404)

        for k, v in all_reviews.items():
            if getattr(v, 'place_id') == place_id:
                review_list.append(v.to_dict())

        return jsonify(review_list)

    else:
        abort(404)


@app_views.route("reviews/<review_id>", strict_slashes=False,
                 methods=['GET'])
def review(review_id):
    """Retrieve review object"""
    if review_id is not None:

        single_review = storage.get(Review, review_id)

        if single_review is None:
            abort(404)

        return jsonify(single_review.to_dict())

    else:
        abort(404)


@app_views.route("reviews/<review_id>", strict_slashes=False,
                 methods=['DELETE'])
def review_delete(review_id):
    """Deletes a review object """
    if review_id is not None:
        del_review = storage.get(Review, review_id)

        if del_review is None:
            abort(404)

        del_review.delete()
        storage.save()

        return {}

    else:
        abort(404)


@app_views.route("places/<place_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def review_add(place_id):
    """Add a review object """
    data = request.get_json()

    if data is None:
        err_return = {"error": "Not a JSON"}
        return jsonify(err_return), 400

    if "user_id" not in data:
        err_return = {"error": "Missing user_id"}
        return jsonify(err_return), 400

    if "text" not in data:
        err_return = {"error": "Missing text"}
        return jsonify(err_return), 400

    if place_id is not None:

        single_place = storage.get(Place, place_id)

        if single_place is None:
            abort(404)

        single_user = storage.get(User, data['user_id'])

        if single_user is None:
            abort(404)

        new = Review(**data)

        setattr(new, 'place_id', place_id)
        storage.new(new)
        storage.save()
        return jsonify(new.to_dict()), 201

    else:
        abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=['PUT'])
def review_update(review_id):
    """Update review object """
    data = request.get_json()

    if data is None:
        error_dict = {"error": "Not a JSON"}
        return jsonify(error_dict), 400

    single_review = storage.get(Review, review_id)

    if single_review is None:
        abort(404)

    setattr(single_review, 'text', data['text'])
    single_review.save()
    storage.save()

    return jsonify(single_review.to_dict())
