# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

# standard library
import enum
from pathlib import Path
from datetime import datetime

# third-party
import flask
import flask_restless
import flask_sqlalchemy
import sqlalchemy.orm as orm

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__)
# Tell flask-sqlalchemy how to connect to the database
path_db = Path(__file__).absolute().parent / "app.sqlite"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{path_db}"
# Create the virtual database object (it's a flask-sqlalchemy concepts).
db = flask_sqlalchemy.SQLAlchemy(app)


# Declare data models
#
# - User: a YouTube user
# - Video: a video uploaded by user, one video can have only one user
# - Playlist: a playlist created by user, it could have many videos.
# - User / Video authorship is one-to-many relationship
# - User / Playlist ownership is one-to-many relationship
# - Playlist / Video is many-to-many relationship
class User(db.Model):
    __tablename__ = "user"

    id: orm.Mapped[str] = db.Column(db.Unicode, primary_key=True)
    name: orm.Mapped[str] = db.Column(db.Unicode)
    create_at: orm.Mapped[datetime] = db.Column(db.DateTime)
    update_at: orm.Mapped[datetime] = db.Column(db.DateTime)
    deleted: orm.Mapped[int] = db.Column(db.Integer)


# for many-to-many relationship, define an association table
# and then pick one of the involved entity model, set a relationship there
# in this example, we will set a relationship in Playlist at videos attribute
playlist_video = db.Table(
    # table name doesn't matter
    "playlist_video",
    db.Column(
        # column name doesn't matter
        "playlist_id",
        db.Unicode,
        # foreign key does matter, it should be ${table_name}.${primary_key_name}
        db.ForeignKey("playlist.id"),
    ),
    db.Column(
        # column name doesn't matter
        "video_id",
        db.Unicode,
        # foreign key does matter, it should be ${table_name}.${primary_key_name}
        db.ForeignKey("video.id"),
    ),
)


# for one-to-many relationship, define a relationship in the 'many' entity.
# in this example, one user can have many videos, then the 'many' entity is the Video,
# so we will set a relationship in 'Video' at 'author' attribute
class Video(db.Model):
    __tablename__ = "video"

    id: orm.Mapped[str] = db.Column(db.Unicode, primary_key=True)
    title: orm.Mapped[str] = db.Column(db.Unicode)
    create_at: orm.Mapped[datetime] = db.Column(db.DateTime)
    update_at: orm.Mapped[datetime] = db.Column(db.DateTime)
    deleted: orm.Mapped[int] = db.Column(db.Integer)
    author_id: orm.Mapped[str] = db.Column(db.Unicode, db.ForeignKey("user.id"))

    # This is not a column, it is a relationship
    author: orm.Mapped[User] = db.relationship(
        User,
        # backref will generate a new attribute (not column) in User model
        # you can use this attribute to get all videos uploaded by this user.
        # note that you have to declare this backref attribute in User model
        # with original sqlalchemy.orm
        # (see example: https://github.com/MacHu-GWU/learn_sqlalchemy-project/blob/master/docs/source/02-orm/02-relationship-configuration/02-one-to-many/e1_simple_one_to_many.py#L23)
        # but you don't do (you cannot) this and flask-sqlalchemy will do this for you
        backref=db.backref("owned_videos"),
    )


class Playlist(db.Model):
    __tablename__ = "playlist"

    id: orm.Mapped[str] = db.Column(db.Unicode, primary_key=True)
    title: orm.Mapped[str] = db.Column(db.Unicode)
    create_at: orm.Mapped[datetime] = db.Column(db.DateTime)
    update_at: orm.Mapped[datetime] = db.Column(db.DateTime)
    deleted: orm.Mapped[int] = db.Column(db.Integer)
    owner_id: orm.Mapped[str] = db.Column(db.Unicode, db.ForeignKey("user.id"))

    # this one is similar to Video.author
    owner: orm.Mapped[User] = db.relationship(
        User, backref=db.backref("owned_playlists")
    )
    # backref will generate a new attribute (not column) in Video model
    # you can use this attribute to get all playlists that include this video.
    # note that you have to declare this backref attribute in Video model
    # with original sqlalchemy.orm
    # (see example: https://github.com/MacHu-GWU/learn_sqlalchemy-project/blob/master/docs/source/02-orm/02-relationship-configuration/03-many-to-many/e1_many_to_many.py#L51)
    # but you don't do (you cannot) this and flask-sqlalchemy will do this for you
    videos = db.relationship(
        Video,
        # for many-to-many, use secondary to specify the association table
        secondary=playlist_video,
        backref="playlists",
    )


# Define an enumeration for the type of entity.
class EntityTypeEnum(str, enum.Enum):
    user = "user"
    video = "video"
    playlist = "playlist"


ETE = EntityTypeEnum


# Create the database tables.
with app.app_context():
    db.create_all()

    # Create the Flask-Restless API manager.
    manager = flask_restless.APIManager(app, session=db.session)

    # Create API endpoints, which will be available at /api/<tablename> by
    # default. Allowed HTTP methods can be specified as well.
    manager.create_api(
        User,
        methods=["GET", "POST", "PATCH", "DELETE"],
        # if you use auto-increment integer primary key, you should set allow_client_generated_ids=False
        # if you use string primary key, you can set allow_client_generated_ids=True
        allow_client_generated_ids=True,
    )
    manager.create_api(
        Video,
        # Get = retrieve
        # Post = create
        # Patch = update
        # Delete = delete
        methods=["GET", "POST", "PATCH", "DELETE"],
        allow_client_generated_ids=True,
        # if you want to replace many videos owned by a user
        # or many videos in a playlist in one API call, you should set allow_to_many_replacement=True
        allow_to_many_replacement=True,
    )
    manager.create_api(
        Playlist,
        methods=["GET", "POST", "PATCH", "DELETE"],
        allow_client_generated_ids=True,
        allow_to_many_replacement=True,
    )
