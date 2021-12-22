from flask_login import login_required, current_user
from flask import session, url_for, render_template,abort, redirect
from application.models import *
from .forms import *
from . import blog


@blog.route("/new_post",methods=['POST','GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.text.data,
                    author_id=current_user.id,
                    author_name=current_user.name,
                    species_id=int(form.categories.data))
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.show_posts',page=1))
    else:
        return render_template("blog/edit_post.html",form=form)


@blog.route("/show_post/<int:page_id>",methods=['GET'])
@login_required
def show_post(page_id):
    post = Post.query.filter_by(id=page_id).first()
    collect = Collect.query.filter_by(collect_user_id=current_user.id,collect_post_id=post.id).first()
    collected = False
    if collect :
        collected = True
    return render_template("blog/singal_post.html",post=post,collected=collected)


@blog.route("/show_posts/<int:page>",methods=['GET'])
@login_required
def show_posts(page):
    if not page:
        page = 1
    pagination = Post.query.filter_by().order_by(Post.timestmp.desc()).paginate(page=page,per_page=10)
    posts = pagination.items
    species = Species.query.all()
    return render_template("blog/posts.html",posts=posts,pagination=pagination,endpoint="blog.show_posts",species=species)


@blog.route("/show_works/<int:page>",methods=['GET'])
@login_required
def show_works(page):
    if not page:
        page = 1
    pagination = Homework.query.filter_by().order_by(Homework.timestmp.desc()).paginate(page=int(page),per_page=10)
    posts = pagination.items
    species = Species.query.all()
    return render_template("main/works.html",posts=posts,pagination=pagination,endpoint="blog.show_works",species=species)


@blog.route("/show_posts/<int:page>/<string:name>",methods=['GET'])
@login_required
def show_species_posts(page,name):
    if not page:
        page = 1
    pagination = None
    posts = None
    species_all = None
    try:
        species = Species.query.filter_by(name=name).first()
        pagination = Post.query.filter_by(species_id=species.id).order_by(Post.timestmp.desc()).paginate(page=page,per_page=10)
        posts = pagination.items
        species_all = Species.query.all()
    except:
        current_app.logger.error("查询文章表失败")

    return render_template("blog/species_posts.html",posts=posts,pagination=pagination,endpoint="blog.show_species_posts",species=species_all,name=name)


@blog.route("/show_works/<int:page>/<string:name>",methods=['GET'])
@login_required
def show_species_works(page,name):
    if not page:
        page = 1
    pagination = None
    posts = None
    species_all = None
    try:
        species = Species.query.filter_by(name=name).first()
        pagination = Homework.query.filter_by(species_id=species.id).order_by(Homework.timestmp.desc()).paginate(page=page,per_page=10)
        posts = pagination.items
        species_all = Species.query.all()
    except:
        current_app.logger.error("查询文章表失败")

    return render_template("main/species_works.html",posts=posts,pagination=pagination,endpoint="blog.show_species_works",species=species_all,name=name)


@blog.route("/show/work/<int:works_id>")
@login_required
def show_work(works_id):
    homework = Homework.query.filter_by(id=works_id).first()
    return render_template("blog/singal_work_index.html",post=homework)


@blog.route("/show/admin_work/<int:works_id>")
@login_required
def show_work_admin(works_id):
    homework = Homework.query.filter_by(id=works_id).first()
    return render_template("blog/singal_work_admin.html",post=homework)