from flask import Blueprint
from flaskapp.sqlite_database import  db
from flaskapp.train.service import init_db

bp = Blueprint("util", __name__)

@bp.cli.command("init-db")
def init_db_command():
    init_db(db)