# -*- coding: utf-8 -*-

import typing as T
import flask
import flask_sqlalchemy

from ..constants import FLASK_APP_NAME
from .sqlite_db import PATH_SQLITE_DB


def create_app() -> T.Tuple[flask.Flask, flask_sqlalchemy.SQLAlchemy]:
    app = flask.Flask(FLASK_APP_NAME)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{PATH_SQLITE_DB}"
    db = flask_sqlalchemy.SQLAlchemy(app)
    return app, db
