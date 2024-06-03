# -*- coding: utf-8 -*-

# standard library
import enum
from datetime import datetime

# third-party
import sqlalchemy.orm as orm

from .init_app import app, db


# Define an enumeration for the type of entity.
class EntityTypeEnum(str, enum.Enum):
    prompt_group = "prompt_group"
    prompt = "prompt"
    prompt_version = "prompt_version"


class OneToManyRelationshipTypeEnum(str, enum.Enum):
    prompt_group_and_prompt = "prompt_group_and_prompt"
    prompt_and_prompt_version = "prompt_and_prompt_version"


ETE = EntityTypeEnum
OTMTE = OneToManyRelationshipTypeEnum


# Declare ORM models
class PromptGroup(db.Model):
    __tablename__ = EntityTypeEnum.prompt_group.value

    id: orm.Mapped[str] = db.Column(db.Unicode, primary_key=True)
    name: orm.Mapped[str] = db.Column(db.Unicode, unique=True)
    description: orm.Mapped[str] = db.Column(db.Unicode)
    create_at: orm.Mapped[datetime] = db.Column(db.DateTime)
    update_at: orm.Mapped[datetime] = db.Column(db.DateTime)
    deleted: orm.Mapped[int] = db.Column(db.Integer)


class Prompt(db.Model):
    __tablename__ = EntityTypeEnum.prompt.value

    id: orm.Mapped[str] = db.Column(db.Unicode, primary_key=True)
    name: orm.Mapped[str] = db.Column(db.Unicode, unique=True)
    description: orm.Mapped[str] = db.Column(db.Unicode)
    create_at: orm.Mapped[datetime] = db.Column(db.DateTime)
    update_at: orm.Mapped[datetime] = db.Column(db.DateTime)
    deleted: orm.Mapped[int] = db.Column(db.Integer)

    group_id: orm.Mapped[str] = db.Column(db.Unicode, db.ForeignKey("prompt_group.id"))

    # relationship
    group: orm.Mapped[PromptGroup] = db.relationship(
        PromptGroup, backref=db.backref("prompts")
    )


class PromptVersion(db.Model):
    __tablename__ = EntityTypeEnum.prompt_version.value

    id: orm.Mapped[str] = db.Column(db.Unicode, primary_key=True)
    version: orm.Mapped[int] = db.Column(db.Integer)
    description: orm.Mapped[str] = db.Column(db.Unicode)
    create_at: orm.Mapped[datetime] = db.Column(db.DateTime)
    update_at: orm.Mapped[datetime] = db.Column(db.DateTime)
    deleted: orm.Mapped[int] = db.Column(db.Integer)
    body: orm.Mapped[str] = db.Column(db.Unicode)
    vars: orm.Mapped[str] = db.Column(db.JSON)

    prompt_id: orm.Mapped[str] = db.Column(db.Unicode, db.ForeignKey("prompt.id"))

    # relationship
    prompt: orm.Mapped[Prompt] = db.relationship(Prompt, backref=db.backref("versions"))
