# -*- coding: utf-8 -*-

import typing as T
import json
import uuid
import requests
from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm

from rich import print as rprint
from rich.console import Console
from rich.panel import Panel

from prompt_ide.app.sqlite_db import PATH_SQLITE_DB
from prompt_ide.app.model import (
    PromptGroup,
    Prompt,
    PromptVersion,
    ETE,
    OTMTE,
)
from prompt_ide.app.api_client import Api

engine = sa.create_engine(f"sqlite:///{PATH_SQLITE_DB}")

host = "http://127.0.0.1:5000"

console = Console()

api = Api(host=host, verbose=True)


def clear_data():
    with engine.connect() as conn:
        conn.execute(PromptGroup.__table__.delete())
        conn.execute(Prompt.__table__.delete())
        conn.execute(PromptVersion.__table__.delete())
        conn.commit()


clear_data()


# ------------------------------------------------------------------------------
# Create Dummy Data
# ------------------------------------------------------------------------------
rprint(Panel("Create Dummy Data"))

default_prompt_group = api.prompt_group.create(name="default")
console.rule("default_prompt_group")
rprint(default_prompt_group)

summarize_prompt = api.prompt.create(group_id=default_prompt_group.id, name="summarize")
console.rule("summarize_prompt")
rprint(summarize_prompt)

tell_joke_prompt = api.prompt.create(group_id=default_prompt_group.id, name="tell joke")
console.rule("tell_joke_prompt")
rprint(tell_joke_prompt)

summarize_prompt_v1 = api.prompt_version.create(
    prompt_id=summarize_prompt.id,
    body="summarize this v1: {user_data}",
    vars={"user_data": {"type": "str"}},
)
console.rule("summarize_prompt_v1")
rprint(summarize_prompt_v1)

summarize_prompt_v2 = api.prompt_version.create(
    prompt_id=summarize_prompt.id,
    body="summarize this v2: {user_data}",
    vars={"user_data": {"type": "str"}},
)
console.rule("summarize_prompt_v2")
rprint(summarize_prompt_v2)

summarize_prompt_v3 = api.prompt_version.create(
    prompt_id=summarize_prompt.id,
    body="summarize this v3: {user_data}",
    vars={"user_data": {"type": "str"}},
)
console.rule("summarize_prompt_v3")
rprint(summarize_prompt_v3)

tell_joke_prompt_v1 = api.prompt_version.create(
    prompt_id=tell_joke_prompt.id,
    body="tell me a joke v1",
    vars={},
)
console.rule("tell_joke_prompt_v1")
rprint(tell_joke_prompt_v1)

tell_joke_prompt_v2 = api.prompt_version.create(
    prompt_id=tell_joke_prompt.id,
    body="tell me a joke v2",
    vars={},
)
console.rule("tell_joke_prompt_v2")
rprint(tell_joke_prompt_v2)

summarize_prompt_versions = api.prompt_version.list_versions(
    prompt_id=summarize_prompt.id
)
console.rule("summarize_prompt_versions")
rprint(summarize_prompt_versions)

tell_joke_prompt_versions = api.prompt_version.list_versions(
    prompt_id=tell_joke_prompt.id
)
console.rule("tell_joke_prompt_versions")
rprint(tell_joke_prompt_versions)
