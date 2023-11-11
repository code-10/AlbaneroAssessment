from flask import Flask
from flaskapp.logger_config import *
from flaskapp.user_management import models
from flaskapp.train import models

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("flaskapp.config.DevelopmentConfig")

    from .sqlite_database import db
    db.init_app(app)

    from flaskapp.migration_config import migrate
    migrate.init_app(app, db)

    from flaskapp.mongo_database import mdb
    mdb.init_app(app)

    from flaskapp.user_management.auth import login_manager
    login_manager.init_app(app)

    from .user_management import blueprint as user_bp
    from .train import blueprint as train_bp
    from .commands import bp as commands_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(train_bp)
    app.register_blueprint(commands_bp)

    return app
