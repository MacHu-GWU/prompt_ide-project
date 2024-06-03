# -*- coding: utf-8 -*-

import flask_restless
from .model import app, db, Prompt, PromptGroup, PromptVersion

with app.app_context():
    db.create_all()

    # Create the Flask-Restless API manager.
    manager = flask_restless.APIManager(app, session=db.session)

    # Create API endpoints, which will be available at /api/<tablename> by
    # default. Allowed HTTP methods can be specified as well.
    manager.create_api(
        PromptGroup,
        methods=["GET", "POST", "PATCH", "DELETE"],
        # if you use auto-increment integer primary key, you should set allow_client_generated_ids=False
        # if you use string primary key, you can set allow_client_generated_ids=True
        allow_client_generated_ids=True,
    )
    manager.create_api(
        Prompt,
        # NOTE: in enterprise, you may want to disable DELETE
        methods=["GET", "POST", "PATCH", "DELETE"],
        allow_client_generated_ids=True,
        # if you want to replace many prompt owned by a group
        allow_to_many_replacement=True,
    )
    manager.create_api(
        PromptVersion,
        # NOTE: in enterprise, since a version should be immutable,
        # you may want to disable PATCH, DELETE
        methods=["GET", "POST", "PATCH", "DELETE"],
        allow_client_generated_ids=True,
        allow_to_many_replacement=True,
    )
