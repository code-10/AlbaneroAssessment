from flask import Blueprint

blueprint = Blueprint("train", __name__)

from .routes import *