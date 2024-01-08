#!/usr/bin/python3
"""
Views for the api of the project
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__)

from api.v1.views.index import *
