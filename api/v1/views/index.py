#!/usr/bin/python3

"""Creating index page"""
from api.v1.views import app_views
from flask import Flask, render_template, jsonify


@app_views.route("/status", strict_slashes=False)
def index():
    """create a route /status on the object app_views that returns a JSON:"""
    status_dict = {"status": "OK"}
    return (jsonify(status_dict))
