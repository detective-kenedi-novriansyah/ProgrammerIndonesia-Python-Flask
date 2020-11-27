from app.app_post.schema import PostSchema
from app.extension.modules import db, bcrypt
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.models.user import Post, User
from sqlalchemy import desc

from .forms import UpdateUserForm, UserLoginForm, UserRegisterForm
from .schema import UserSchema
from app.app_user.utils import save_profile

blue_print_user = Blueprint('user', __name__)


@blue_print_user.route('/login', methods=["GET", "POST"])
def userLogin():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        check_password = bcrypt.check_password_hash(user.password, form.password.data)
        if user and check_password:
            login_user(user)
            return redirect(url_for('post.post'))
    return render_template("user/login.html", form=form)

@blue_print_user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.userLogin"))

@blue_print_user.route('/user/<int:pk>', methods=["GET", "POST"])
def detailuser(pk):
    form = UpdateUserForm()
    print(form.validate_on_submit())
    user = User.query.get(pk)
    post = Post.query.filter_by(author=user).order_by(desc('id'))
    us = UserSchema()
    ps = PostSchema()
    u_sc = us.dump(user)
    p_sc = ps.dump(post,many=True)
    if form.validate_on_submit():
        if form.profile.data:
            s_image = save_profile(form.profile.data)
            user.profile = s_image
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        return redirect(url_for('user.detailuser', pk=user.id))
    else:
        form.username.data = user.username
        form.email.data = user.email
        form.profile.data = user.profile

    return render_template("user/detailuser.html", user=u_sc,post=p_sc, form=form)


@blue_print_user.route('/register', methods=["GET", "POST"])
def registerUser():
    form = UserRegisterForm()
    if form.validate_on_submit():
        hashs = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data,email=form.email.data,password=hashs)
        db.session.add(user)
        db.session.commit()
        flash("Kamu Berhasil membuat user baru")
        return redirect(url_for("user.userLogin"))
    return render_template("user/register.html", form=form)
