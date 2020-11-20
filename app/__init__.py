import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(base_dir, "db.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app,db)
ma = Marshmallow(app)

from .models.user import User

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password")

data = [
    "Jhon F Kenedi",
    "Kenedi",
    "Ucup",
    "Elizabert"
]

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User(username=username,password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user'))
    return render_template('home/index.html')

@app.route('/about')
def about():
    return render_template('about/index.html')


@app.route('/user', methods=['GET'])
def user():
    users = User.query.all()
    schema = UserSchema()
    user_schema = schema.dump(users,many=True)
    return render_template('user/index.html', user=user_schema)

@app.route('/user/<int:pk>', methods=['GET'])
def detailUser(pk):
    user_ = User.query.filter_by(id=pk).first()
    schema = UserSchema()
    user_schema = schema.dump(user_)
    return render_template('user/detail/index.html', user=user_schema)

@app.route('/post/<value>/', methods=["GET", "POST"])
def post(value):
    return render_template('post/index.html', value=value)