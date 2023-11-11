from flask import Blueprint

blueprint = Blueprint("user_management", __name__, url_prefix="/user_management")

from flaskapp.user_management import routes