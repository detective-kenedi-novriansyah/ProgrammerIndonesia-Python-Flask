import os
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import desc, asc
from paginate_sqlalchemy import paginate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, Email, EqualTo, DataRequired

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))

app.config["SECRET_KEY"] = "dfe700a02d4004f53d588a2075be3b737f2e5ec2"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(base_dir, "db.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app,db)
ma = Marshmallow(app)
login = LoginManager(app)

bcrypt = Bcrypt(app)

from .models.user import User, Post

class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class UserRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self,username):
        user =  User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username sudah ada, silahkan cari yang lain")

    def validate_email(self,email):
        user =  User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email sudah ada, silahkan cari yang lain")

class RecordPost(FlaskForm):
    id = IntegerField()
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password")

class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "content", "author")

data = [
    "Jhon F Kenedi",
    "Kenedi",
    "Ucup",
    "Elizabert"
]


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('home/index.html')

@app.route('/login', methods=["GET", "POST"])
def userLogin():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        check_password = bcrypt.check_password_hash(user.password, form.password.data)
        if user and check_password:
            login_user(user)
            return redirect(url_for('post'))
    return render_template("user/login.html", form=form)

@app.route('/register', methods=["GET", "POST"])
def registerUser():
    form = UserRegisterForm()
    if form.validate_on_submit():
        hashs = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data,email=form.email.data,password=hashs)
        db.session.add(user)
        db.session.commit()
        flash("Kamu Berhasil membuat user baru")
        return redirect(url_for("userLogin"))
    return render_template("user/register.html", form=form)

@app.route('/post', methods=["GET", "POST"])
@login_required
def post():
    post = Post.query.order_by(desc('id'))
    schema = PostSchema()
    post_schema = schema.dump(post, many=True)
    user = current_user
    form = RecordPost()
    if form.validate_on_submit():
        post = Post(content=form.content.data,user_id=user.id)
        db.session.add(post)
        db.session.commit()
        form.content.data = ""
        flash("Kamu berhasil membuat post baru")
        return redirect(url_for("post"))
    return render_template("post/index.html", post=post_schema,form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("userLogin"))

@app.route('/post/<int:pk>/delete', methods=["GET", "DELETE"])
@login_required
def deletePost(pk):
    post = Post.query.get(pk)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("post"))

@app.route('/post/<int:pk>/update', methods=["GET", "POST"])
@login_required
def updatePost(pk):
    post = Post.query.get(pk)
    form = RecordPost()
    if form.validate_on_submit():
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for("post"))
    else:
        form.id.data = post.id
        form.content.data = post.content
    return render_template("post/updatePost.html", form=form)
