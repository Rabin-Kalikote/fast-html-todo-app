# File: /fasthtml-todo/fasthtml-todo/src/routes/__init__.py

from flask import Blueprint

# Initialize the routes blueprint
routes = Blueprint('routes', __name__)

from .todos import *  # Import all routes from todos.py