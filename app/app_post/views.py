from datetime import datetime
from app.extension.modules import db
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.models.user import Post
from sqlalchemy import desc

from .forms import RecordPost
from .schema import PostSchema

blue_print_post = Blueprint('post', __name__)


@blue_print_post.route('/post', methods=["GET", "POST"])
@login_required
def post():
    page = request.args.get('page',1,type=int)
    post = Post.query.order_by(desc('id')).paginate(page=page,per_page=5)
    schema = PostSchema()
    post_schema = schema.dump(post.items, many=True)
    user = current_user
    form = RecordPost()
    if form.validate_on_submit():
        new_post = Post(content=form.content.data,user_id=user.id,update_at=datetime.utcnow())
        db.session.add(new_post)
        db.session.commit()
        form.content.data = ""
        flash("Kamu berhasil membuat post baru")
        return redirect(url_for("post.post"))
    return render_template("post/index.html", post=post_schema,form=form,now=datetime.utcnow(),pagination=post)


@blue_print_post.route('/post/<int:pk>/delete', methods=["GET", "DELETE"])
@login_required
def deletePost(pk):
    post = Post.query.get(pk)
    db.session.delete(post)
    db.session.commit()
    flash("Post berhasil dihapus")
    return redirect(url_for("post.post"))

@blue_print_post.route('/post/<int:pk>/update', methods=["GET", "POST"])
@login_required
def updatePost(pk):
    post = Post.query.get(pk)
    form = RecordPost()
    if form.validate_on_submit():
        post.content = form.content.data
        post.update_at = datetime.utcnow()
        db.session.commit()
        flash("Post berhasil diperbarui")
        return redirect(url_for("post.post"))
    else:
        form.id.data = post.id
        form.content.data = post.content
    return render_template("post/updatePost.html", form=form)

@blue_print_post.route('/post/<int:pk>', methods=["GET"])
def detailpost(pk):
    post = Post.query.get(pk)
    s = PostSchema()
    ps = s.dump(post)
    return render_template("post/detailpost.html", post=ps)
