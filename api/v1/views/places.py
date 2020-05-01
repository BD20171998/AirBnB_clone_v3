#!/usr/bin/python3
"""State object view """
from flask import Flask, jsonify, request, Response
from flask import abort
from models.state import State
from models.city import City
from models.place import Place
from models import storage
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['GET'])
def places(city_id):
    """retrieve City object(s)"""
    city_list = []

    if city_id is not None:
        all_places = storage.all(City)

        for k, v in all_places.items():
            if getattr(v, 'city_id') == city_id:
                city_list.append(v.to_dict())

        if city_list == [] or city_list is None:
            abort(404)

        return jsonify(city_list)

    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['GET'])
def city(place_id):
    """Retreive city object with city_id"""
    if place_id is not None:

        single_place = storage.get(Place, place_id)

        if single_place is None:
            abort(404)

        return jsonify(single_place.to_dict())

    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['DELETE'])
def city_delete(place_id):
    """Deletes a city object """
    if place_id is not None:
        del_place = storage.get(Place, place_id)

        if del_place is None:
            abort(404)

        return {}

    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['POST'])
def place_add(place_id):
    """Adds a city object"""
    data = request.get_json()

    if data is None:
        err_return = {"error": "Not a JSON"}
        return jsonify(err_return), 400

    if "user_id" not in data:
        err_return = {"error": "Missing name user_id"}
        return jsonify(err_return), 400

    if place_id is not None:

        single_place = storage.get(State, place_id)

        if single_place is None:
            abort(404)

        new = Place(**data)

        setattr(new, 'place_id', place_id)
        storage.new(new)
        storage.save()
        return jsonify(new.to_dict()), 201

    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=['PUT'])
def city_update(place_id):
    """Update a city object"""
    data = request.get_json()

    if data is None:
        error_dict = {"error": "Not a JSON"}
        return jsonify(error_dict), 400

    single_place = storage.get(Place, place_id)

    if single_place is None:
        abort(404)

    setattr(single_place, 'name', data['name'])
    single_place.save()
    storage.save()

    return jsonify(single_place.to_dict())
