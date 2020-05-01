#!/usr/bin/python3
"""State object view """
from flask import Flask, jsonify, request, Response
from models.state import State
from models import storage
from api.v1.views import app_views
@app_views.route("/states", strict_slashes=False,  methods=['GET'])
def states():
    """retrieve State object(s)"""
    state_list = []
    all_states = storage.all(State)
    for k,v in all_states.items():
        state_list.append(v.to_dict())
    return jsonify(state_list)
@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def state_id(state_id):
    """Retrieves a State object based on id"""
    if state_id is not None:
        single_state = storage.get(State, state_id)
        single_state_dict = single_state.to_dict()
        return jsonify(single_state_dict)
@app_views.route("/states/<state_id>", strict_slashes=False, methods=['DELETE'])
def state_delete(state_id):
    """Deletes a state object"""
    if state_id is not None:
        cities_del = storage.all("City")
        for i in cities_del.values():
            if state_id == getattr(i, "state_id"):
                i.delete()
                storage.save()
        state_del = storage.get('State', state_id)
        state_del.delete()
        storage.save()
        return {}
@app_views.route("/states", strict_slashes=False, methods=['POST'])
def state_add():
    """Adds a state object"""
    data = request.get_json()
    new = State(**data)
    new.save()
    storage.save()
    status_code = Response(status=201)
    return status_code
@app_views.route("/states/<state_id>", strict_slashes=False, methods=['PUT'])
def state_update(state_id):
    """Update an existing state object"""
    data = request.get_json()
    single_state = storage.get(State, state_id)
    single_state(**data)
    single_state.save()
    storage.save()
    new = single_state.to_dict()
