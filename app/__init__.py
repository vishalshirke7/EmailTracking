from flask import Flask, render_template, session
from flask_migrate import Migrate

import os
import logging

from .models import db
from app import views
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('dev_config.py', silent=True)
    logger = logging.getLogger('werkzeug')
    formatter = logging.Formatter(
        """%(message)s"""
    )
    handler = logging.FileHandler('access.log')
    logging.StreamHandler()
    logger.addHandler(handler)
    # print(logger.info())
    db.init_app(app)
    migrate = Migrate(app, db)
    app.register_blueprint(views.bp)

    return app