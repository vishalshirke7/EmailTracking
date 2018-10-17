from flask import Flask, render_template, session
from flask_migrate import Migrate
from Scripts.Hyrelabs.app.models import User
import os
from flask import Blueprint, url_for, redirect, render_template, session, request
from flask import jsonify, json
from sqlalchemy import and_
import datetime
from Scripts.Hyrelabs.app.db import db
from Scripts.Hyrelabs.app.models import User
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError
from Scripts.Hyrelabs import config
import logging
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    # app.secret_key = b'\xa9||/\x9dp\x1b\x9f'
    app.config.from_pyfile('dev_config.py', silent=True)
    # setup_logging(app)
    logger = logging.getLogger('werkzeug')
    formatter = logging.Formatter(
        """%(message)s"""
    )
    handler = logging.FileHandler('access.log')
    logging.StreamHandler()
    logger.addHandler(handler)
    # print(logger.info())
    from Scripts.Hyrelabs.app.models import db
    db.init_app(app)
    migrate = Migrate(app, db)

    from Scripts.Hyrelabs.app import views

    app.register_blueprint(views.bp)

    return app