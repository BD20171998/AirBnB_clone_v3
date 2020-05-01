#!/usr/bin/python3
"""User object view """
from flask import Flask, jsonify, request, Response
from flask import abort
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route("/users", strict_slashes=False,  methods=['GET'])
def users():
    """retrieve User object(s)"""
    user_list = []
    all_users = storage.all(User)
    for k, v in all_users.items():
        user_list.append(v.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<user_id>",
                 strict_slashes=False, methods=['GET'])
def user_id(user_id):
    """Retrieves a User object based on id"""
    if user_id is not None:
        single_user = storage.get("User", user_id)
        if single_user is None:
            abort(404)
        single_user_dict = single_user.to_dict()
        return jsonify(single_user_dict)
    else:
        abort(404)


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['DELETE'])
def user_delete(user_id):
    """Deletes a user object"""
    if user_id is not None:
        del_user = storage.get("User", user_id)
        if del_user is None:
            abort(404)

        del_user.delete()
        storage.save()
        ret_del_user = {}
        return jsonify(ret_del_user), 200

    else:
        abort(404)


@app_views.route("/users", strict_slashes=False, methods=['POST'])
def user_add():
    """Adds a user object"""
    data = request.get_json()
    if data is None:
        err_return = {"error": "Not a JSON"}
        return jsonify(err_return), 400
    elif "email" not in data:
        err_return = {"error": "Missing email"}
        return jsonify(err_return), 400
    elif "password" not in data:
        return jsonify({"error": "Missing password"}), 400
    new = User(**data)
    storage.new(new)
    storage.save()
    status_code = 201
    new_user_dict = new.to_dict()
    return jsonify(new_user_dict), status_code


@app_views.route("/users/<user_id>",
                 strict_slashes=False, methods=['PUT'])
def user_update(user_id):
    """Update an existing user object"""
    data = request.get_json()
    if data is None:
        error_dict = {"error": "Not a JSON"}
        return jsonify(error_dict), 400
    single_user = storage.get("User", user_id)
    if single_user is None:
        abort(404)

    if 'first_name' in data:
        setattr(single_user, 'first_name', data['first_name'])

    if 'last_name' in data:
        setattr(single_user, 'last_name', data['last_name'])

    if 'password' in data:
        setattr(single_user, 'password', data['password'])

    single_user.save()
    storage.save()

    return jsonify(single_user.to_dict()), 200
