#!/usr/bin/python3
"""State object view """
from flask import Flask, jsonify, request, Response
from flask import abort
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route("/states", strict_slashes=False,  methods=['GET'])
def states():
    """retrieve State object(s)"""
    state_list = []
    all_states = storage.all(State)
    for k, v in all_states.items():
        state_list.append(v.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def state_id(state_id):
    """Retrieves a State object based on id"""
    if state_id is not None:
        single_state = storage.get("State", state_id)
        if single_state is None:
            abort(404)
        single_state_dict = single_state.to_dict()
        return jsonify(single_state_dict)
    else:
        abort(404)


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=['DELETE'])
def state_delete(state_id):
    """Deletes a state object"""
    if state_id is not None:
        del_state = storage.get("State", state_id)
        if del_state is None:
            abort(404)

        del_state.delete()
        storage.save()

        ret_del_state = {}
        return jsonify(ret_del_state)

    else:
        abort(404)


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def state_add():
    """Adds a state object"""
    data = request.get_json()
    if data is None:
        err_return = {"error": "Not a JSON"}
        return jsonify(err_return), 400
    if "name" not in data:
        err_return = {"error": "Missing name"}
        return jsonify(err_return), 400
    new = State(**data)
    storage.new(new)
    storage.save()
    status_code = 201
    new_state_dict = new.to_dict()
    return jsonify(new_state_dict), status_code


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['PUT'])
def state_update(state_id):
    """Update an existing state object"""
    data = request.get_json()
    if data is None:
        error_dict = {"error": "Not a JSON"}
        return jsonify(error_dict), 400
    single_state = storage.get("State", state_id)
    if single_state is None:
        abort(404)

    setattr(single_state, 'name', data['name'])
    single_state.save()
    storage.save()

    return jsonify(single_state.to_dict())
