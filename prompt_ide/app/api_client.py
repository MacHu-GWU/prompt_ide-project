# -*- coding: utf-8 -*-

import typing as T
import json
import uuid
import dataclasses
from datetime import datetime

import requests
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from ..vendor.better_dataclass import DataClass, T_DATA_LIKE

from .model import ETE, OTMTE

console = Console()


def get_utc_now():
    return datetime.utcnow()


def resolve_verbose(arg: T.Optional[bool], config: bool):
    if arg is None:
        return config
    else:
        return arg


post_headers = {
    "Content-Type": "application/vnd.api+json",
    "Accept": "application/vnd.api+json",
}
get_headers = {
    "Accept": "application/vnd.api+json",
}


def make_request(
    meth: T.Callable, kwargs: T.Dict[str, T.Any], verbose: bool = False
) -> requests.Response:
    """
    A helper function that make HTTP request, and automatically print request and response.
    """
    if verbose:
        console.rule("API Request")
        rprint(kwargs)

    response: requests.Response = meth(**kwargs)
    if verbose:
        console.rule("API Response status code")
        rprint(f"{response.status_code = }")
        console.rule("API Response headers")
        rprint(dict(response.headers))
        console.rule("API Response data")
    if response.status_code in [200, 201]:
        if verbose:
            rprint(json.loads(response.text))
    elif response.status_code == 204:
        if verbose:
            print("No content")
    else:
        if verbose:
            rprint(response.text)
    return response


@dataclasses.dataclass
class Resource:
    host: str = dataclasses.field()
    name: str = dataclasses.field()
    verbose: bool = dataclasses.field(default=False)

    @property
    def endpoint(self):
        return f"{self.host}/api/{self.name}"


@dataclasses.dataclass
class PromptGroupData(DataClass):
    id: str
    name: str
    description: str
    create_at: datetime
    update_at: datetime
    deleted: int


@dataclasses.dataclass
class PromptGroup(Resource):
    def create(
        self,
        name: str,
        description: str = "no description",
        verbose: T.Optional[bool] = None,
    ):
        utc_now = get_utc_now()
        data = {
            "data": {
                "type": self.name,
                "id": str(uuid.uuid4()),
                "attributes": {
                    "name": name,
                    "description": description,
                    "create_at": utc_now.isoformat(),
                    "update_at": utc_now.isoformat(),
                    "deleted": 0,
                },
            },
        }
        kwargs = dict(
            url=self.endpoint,
            headers=post_headers,
            json=data,
        )
        verbose = resolve_verbose(verbose, self.verbose)
        response = make_request(requests.post, kwargs, verbose=verbose)
        if response.status_code == 201:
            res_data = response.json()
            return PromptGroupData(
                id=res_data["data"]["id"],
                name=res_data["data"]["attributes"]["name"],
                description=res_data["data"]["attributes"]["description"],
                create_at=res_data["data"]["attributes"]["create_at"],
                update_at=res_data["data"]["attributes"]["update_at"],
                deleted=res_data["data"]["attributes"]["deleted"],
            )
        else:
            return None


@dataclasses.dataclass
class PromptData(DataClass):
    id: str
    name: str
    description: str
    create_at: datetime
    update_at: datetime
    deleted: int
    group_id: str


@dataclasses.dataclass
class Prompt(Resource):
    def create(
        self,
        group_id,
        name: str,
        description: str = "no description",
        verbose: T.Optional[bool] = None,
    ):
        utc_now = get_utc_now()
        data = {
            "data": {
                "type": self.name,
                "id": str(uuid.uuid4()),
                "attributes": {
                    "name": name,
                    "description": description,
                    "create_at": utc_now.isoformat(),
                    "update_at": utc_now.isoformat(),
                    "deleted": 0,
                    "group_id": group_id,
                },
            },
        }
        kwargs = dict(
            url=self.endpoint,
            headers=post_headers,
            json=data,
        )
        verbose = resolve_verbose(verbose, self.verbose)
        response = make_request(requests.post, kwargs, verbose=verbose)
        if response.status_code == 201:
            res_data = response.json()
            return PromptData(
                id=res_data["data"]["id"],
                name=res_data["data"]["attributes"]["name"],
                description=res_data["data"]["attributes"]["description"],
                create_at=res_data["data"]["attributes"]["create_at"],
                update_at=res_data["data"]["attributes"]["update_at"],
                deleted=res_data["data"]["attributes"]["deleted"],
                group_id=res_data["data"]["relationships"]["group"]["data"]["id"],
            )
        else:
            return None


@dataclasses.dataclass
class PromptVersionData(DataClass):
    id: str
    description: str
    create_at: datetime
    update_at: datetime
    deleted: int
    body: str
    vars: T.Optional[T.Dict[str, T.Any]]
    prompt_id: str


@dataclasses.dataclass
class PromptVersion(Resource):
    def create(
        self,
        prompt_id: str,
        body: str,
        vars: T.Optional[T.Dict[str, T.Any]] = None,
        description: str = "no description",
        verbose: T.Optional[bool] = None,
    ):
        utc_now = get_utc_now()
        data = {
            "data": {
                "type": self.name,
                "id": str(uuid.uuid4()),
                "attributes": {
                    "description": description,
                    "create_at": utc_now.isoformat(),
                    "update_at": utc_now.isoformat(),
                    "deleted": 0,
                    "body": body,
                    "vars": vars,
                    "prompt_id": prompt_id,
                },
            },
        }
        kwargs = dict(
            url=self.endpoint,
            headers=post_headers,
            json=data,
        )
        verbose = resolve_verbose(verbose, self.verbose)
        response = make_request(requests.post, kwargs, verbose=verbose)
        if response.status_code == 201:
            res_data = response.json()
            return PromptVersionData(
                id=res_data["data"]["id"],
                description=res_data["data"]["attributes"]["description"],
                create_at=res_data["data"]["attributes"]["create_at"],
                update_at=res_data["data"]["attributes"]["update_at"],
                deleted=res_data["data"]["attributes"]["deleted"],
                body=res_data["data"]["attributes"]["body"],
                vars=res_data["data"]["attributes"]["vars"],
                prompt_id=res_data["data"]["relationships"]["prompt"]["data"]["id"],
            )
        else:
            return None

    def list_versions(
        self,
        prompt_id: str,
        verbose: T.Optional[bool] = None,
    ) -> T.List["PromptVersionData"]:
        filters = [dict(name="prompt_id", op="eq", val=prompt_id)]
        params = {
            "filter[objects]": json.dumps(filters),
            "sort": "-create_at",
        }
        kwargs = dict(
            url=self.endpoint,
            headers=post_headers,
            params=params,
        )
        verbose = resolve_verbose(verbose, self.verbose)
        response = make_request(requests.get, kwargs, verbose=verbose)
        if response.status_code == 200:
            res_data = response.json()
            return [
                PromptVersionData(
                    id=dct["id"],
                    description=dct["attributes"]["description"],
                    create_at=dct["attributes"]["create_at"],
                    update_at=dct["attributes"]["update_at"],
                    deleted=dct["attributes"]["deleted"],
                    body=dct["attributes"]["body"],
                    vars=dct["attributes"]["vars"],
                    prompt_id=dct["relationships"]["prompt"]["data"]["id"],
                )
                for dct in res_data["data"]
            ]
        else:
            return []

@dataclasses.dataclass
class Api:
    # fmt: off
    host: str = dataclasses.field()
    verbose: bool = dataclasses.field(default=False)

    prompt_group: PromptGroup = dataclasses.field(init=False)
    prompt: Prompt = dataclasses.field(init=False)
    # prompt_alias: PromptAlias = dataclasses.field(init=False)

    def __post_init__(self):
        self.prompt_group = PromptGroup(host=self.host, name=ETE.prompt_group.value, verbose=self.verbose)
        self.prompt = Prompt(host=self.host, name=ETE.prompt.value, verbose=self.verbose)
        self.prompt_version = PromptVersion(host=self.host, name=ETE.prompt_version.value, verbose=self.verbose)
    # fmt: on
