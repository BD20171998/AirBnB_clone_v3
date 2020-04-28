#!/usr/bin/python3

"""Creating index page"""
from api.v1.views import app_views
from flask import render_template

@app_views.route("/status")
def app_views():
    """create a route /status on the object app_views that returns a JSON:"""
    return {"status": "OK"}
