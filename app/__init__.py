import os

from flask import Flask
from .extension.modules import extension


def create_app():


    app = Flask(__name__)

    base_dir = os.path.abspath(os.path.dirname(__file__))

    app.config["SECRET_KEY"] = "dfe700a02d4004f53d588a2075be3b737f2e5ec2"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(base_dir, "db.sqlite")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    extension(app)
    return app

