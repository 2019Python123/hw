from flask_login import login_required, current_user
from flask import session, url_for, render_template,abort, redirect
from application.models import *
from .forms import *
from . import blog


@blog.route("/new_post",methods=['POST','GET'])
@login_required
def new_post():
    """
    发布博客
    :return:
    """
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
    """
    显示单个的博客内容
    :param page_id:
    :return:
    """
    post = Post.query.filter_by(id=page_id).first()
    collect = Collect.query.filter_by(collect_user_id=current_user.id,collect_post_id=post.id).first()
    collected = False
    if collect :
        collected = True
    return render_template("blog/singal_post.html",post=post,collected=collected)


@blog.route("/show_posts/<int:page>",methods=['GET'])
@login_required
def show_posts(page):
    """
    显示所有文章
    :param page:
    :return:
    """
    if not page:
        page = 1
    pagination = Post.query.filter_by().order_by(Post.timestmp.desc()).paginate(page=page,per_page=10)
    posts = pagination.items
    species = Species.query.all()
    return render_template("blog/posts.html",posts=posts,pagination=pagination,endpoint="blog.show_posts",species=species)


@blog.route("/show_works/<int:page>",methods=['GET'])
@login_required
def show_works(page):
    """
    在首页显示所有作业
    :param page:
    :return:
    """
    if not page:
        page = 1
    pagination = Homework.query.filter_by().order_by(Homework.timestmp.desc()).paginate(page=int(page),per_page=10)
    posts = pagination.items
    species = Species.query.all()
    return render_template("main/works.html",posts=posts,pagination=pagination,endpoint="blog.show_works",species=species)


@blog.route("/show_posts/<int:page>/<string:name>",methods=['GET'])
@login_required
def show_species_posts(page,name):
    """
    实现点击标签超链接，显示不同标签的文章
    :param page:
    :param name:
    :return:
    """
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
    """
    实现点击标签超链接，显示不同标签的作业
    :param page:
    :param name:
    :return:
    """
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
    """
    显示单个作业内容
    :param works_id:
    :return:
    """
    homework = Homework.query.filter_by(id=works_id).first()
    hu = HomeWork_User.query.filter_by(owner_name=current_user.name,homework_id=homework.id).first()
    return render_template("blog/singal_work.html",post=homework,is_owner=True if hu is not None else False)


@blog.route("/show/admin_work/<int:works_id>")
@login_required
def show_work_admin(works_id):
    """
    后台管理显示单个作业内容
    :param works_id:
    :return:
    """
    homework = Homework.query.filter_by(id=works_id).first()

    return render_template("blog/singal_work_admin.html",post=homework)