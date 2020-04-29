#!/usr/bin/python3

"""Creating index page"""
from api.v1.views.__init__ import app_views
from flask import Flask, render_template

@app_views.route("/status", strict_slashes=False)
def app_views():
    """create a route /status on the object app_views that returns a JSON:"""

    return {"status": "OK"}
