#!/usr/bin/python3

"""creating blueprint """
from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint(__name__, url_prefix='/api/v1')
