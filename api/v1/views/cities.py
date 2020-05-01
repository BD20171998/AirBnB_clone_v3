#!/usr/bin/python3
"""State object view """
from flask import Flask, jsonify, request, Response
from flask import abort
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def cities(state_id):
    """retrieve City object(s)"""
    city_list = []

    if state_id is not None:
        all_cities = storage.all(City)

        single_state = storage.get(State, state_id)

        if single_state is None:
            abort(404)

        for k, v in all_cities.items():
            if getattr(v, 'state_id') == state_id:
                city_list.append(v.to_dict())

        return jsonify(city_list)

    else:
        abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=['GET'])
def city(city_id):
    """Retreive city object with city_id"""
    if city_id is not None:
        all_cities = storage.all(City)

        single_city = storage.get(City, city_id)

        if single_city is None:
            abort(404)

        return jsonify(single_city.to_dict())

    else:
        abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=['DELETE'])
def city_delete(city_id):
    """Deletes a city object """
    if city_id is not None:
        del_city = storage.get(City, city_id)

        if del_city is None:
            abort(404)

        del_city.delete()
        storage.save()
        return {}

    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['POST'])
def city_add(state_id):
    """Adds a city object"""
    data = request.get_json()

    if data is None:
        err_return = {"error": "Not a JSON"}
        return jsonify(err_return), 400

    if "name" not in data:
        err_return = {"error": "Missing name"}
        return jsonify(err_return), 400

    if state_id is not None:

        single_state = storage.get(State, state_id)

        if single_state is None:
            abort(404)

        new = City(**data)

        setattr(new, 'state_id', state_id)
        storage.new(new)
        storage.save()
        return jsonify(new.to_dict()), 201

    else:
        abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['PUT'])
def city_update(city_id):
    """Update a city object"""
    data = request.get_json()

    if data is None:
        error_dict = {"error": "Not a JSON"}
        return jsonify(error_dict), 400

    single_city = storage.get(City, city_id)

    if single_city is None:
        abort(404)

    setattr(single_city, 'name', data['name'])
    single_city.save()
    storage.save()

    return jsonify(single_city.to_dict())
