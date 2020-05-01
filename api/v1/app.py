#!/usr/bin/python3
"""
 API
"""
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def end_session(response_or_exc):
    """"Ends DB session  """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """  404  """
    status = {"error": "Not found"}
    return jsonify(status), 404


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
