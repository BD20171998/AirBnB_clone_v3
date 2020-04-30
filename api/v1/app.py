#!/usr/bin/python3
""" API """

from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """tear down method"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """Error 404"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    if getenv('HBNB_API_HOST') is not None:
        host = getenv('HBNB_TYPE_HOST')

    else:
        host = '0.0.0.0'

    if getenv('HBNB_API_PORT') is not None:
        port = getenv('HBNB_API_PORT')

    else:
        port = '5000'

    app.run(host=host, port=port, threaded=True)
