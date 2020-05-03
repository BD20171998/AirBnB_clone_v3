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

        single_city = storage.get(City, city_id)

        if single_city is None:
            abort(404)

        all_places = storage.all(Place)

        for k, v in all_places.items():
            if getattr(v, 'city_id') == city_id:
                city_list.append(v.to_dict())

        return jsonify(city_list)

    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['GET'])
def city_r(place_id):
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
def place_delete(place_id):
    """Deletes a city object """
    if place_id is not None:
        del_place = storage.get("Place", place_id)

        if del_place is None:
            abort(404)

        del_place.delete()
        storage.save()
        return {}

    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['POST'])
def place_add(city_id):
    """Adds a city object"""
    data = request.get_json()

    if data is None:
        err_return = {"error": "Not a JSON"}
        return jsonify(err_return), 400

    if "user_id" not in data:
        err_return = {"error": "Missing user_id"}
        return jsonify(err_return), 400

    if "name" not in data:
        err_return = {"error": "Missing name"}
        return jsonify(err_return), 400

    if city_id is not None:

        single_user = storage.get("User", data["user_id"])

        single_city = storage.get("City", city_id)

        if single_user is None:
            abort(404)

        if single_city is None:
            abort(404)

        new = Place(**data)

        setattr(new, 'city_id', city_id)
        storage.new(new)
        storage.save()
        return jsonify(new.to_dict()), 201

    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=['PUT'])
def place_update(place_id):
    """Update a city object"""
    data = request.get_json()

    if data is None:
        error_dict = {"error": "Not a JSON"}
        return jsonify(error_dict), 400

    single_place = storage.get("Place", place_id)

    if single_place is None:
        abort(404)

    if 'description' in data:
        setattr(single_place, 'description', data['description'])

    if 'number_rooms' in data:
        setattr(single_place, 'number_rooms', data['number_rooms'])

    if 'number_bathrooms' in data:
        setattr(single_place, 'number_bathrooms', data['number_bathrooms'])

    if 'max_guest' in data:
        setattr(single_place, 'max_guest', data['max_guest'])

    if 'price_by_night' in data:
        setattr(single_place, 'price_by_night', data['price_by_night'])

    if 'latitude' in data:
        setattr(single_place, 'latitude', data['latitude'])

    if 'longitude' in data:
        setattr(single_place, 'longitude', data['longitude'])

    if 'amenity_ids' in data:
        setattr(single_place, 'amenity_ids', data['amenity_ids'])

    setattr(single_place, 'name', data['name'])
    single_place.save()
    storage.save()

    return jsonify(single_place.to_dict())
