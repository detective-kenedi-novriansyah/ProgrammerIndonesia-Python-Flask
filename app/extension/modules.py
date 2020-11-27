# package Pillow
from flask_moment import Moment
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import desc, asc
from marshmallow import fields
from flask_marshmallow import Marshmallow
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
login = LoginManager()
mm = Moment()
bcrypt = Bcrypt()

from app.app_user.views import blue_print_user
from app.app_post.views import blue_print_post
from app.app_home.views import blue_print_home
from app.models.user import User, Post

def extension(index):
    db.init_app(index)
    migrate.init_app(index,db)
    ma.init_app(index)
    login.init_app(index)
    mm.init_app(index)
    bcrypt.init_app(index)
    index.register_blueprint(blue_print_user)
    index.register_blueprint(blue_print_post)
    index.register_blueprint(blue_print_home)
    