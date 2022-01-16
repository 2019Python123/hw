from . import auth
from flask_login import current_user,login_required,login_user,logout_user
from flask import session,url_for,request,redirect,render_template,current_app,flash
from application.helper import get_file
from application.models import *


@auth.route("/login",methods=['POST','GET'])
def login():
    if request.method == 'POST':
        form = request.form.to_dict()
        user = User.query.filter_by(name=form.get("name")).first()
        if user:
            if user.verify_password_hash(form.get('passwd')) and form.get('yzm').lower() == session['yzm'].lower():
                login_user(user,form.get('remember'))
                flash(form.get('name')+'同学登录成功')
                return redirect(url_for('blog.show_posts',page=1))
            else:
                flash("登录失败请重新登录")
                return redirect(url_for('auth.login'))
        else:
            flash("您不存在，请进行注册")
            return redirect(url_for('auth.logon'))
    if current_user.is_authenticated:
        return redirect(url_for('blog.show_posts',page=1))
    img_src,yzm = get_file("application/static/captcha")
    session['yzm'] = yzm

    return render_template("auth/login.html",img_src=img_src)


@auth.route("/logon",methods=['POST','GET'])
def logon():
    if request.method == 'POST':
        form = request.form.to_dict()
        query_user = User.query.filter_by(name=form.get("name")).first()
        if form.get('yzm').lower() == session['yzm'].lower() and query_user is None:
            user = User(name=form.get('name'),password=form.get("passwd"))
            db.session.add(user)
            db.session.commit()
            flash('恭喜'+form.get('name')+'同学注册成功')
            return redirect(url_for('blog.show_posts',page=1))
        elif query_user:
            flash(form.get("name")+"同学您已经注册过啦,请前往登录")
            return redirect(url_for('auth.login'))
        return redirect(url_for('auth.logon'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('blog.show_posts', page=1))
        img_src, yzm = get_file("application/static/captcha")
        session['yzm'] = yzm
        return render_template('auth/logon.html',img_src=img_src)


@auth.route("/logout")
@login_required
def logout():
    flash(current_user.name+"同学退出登录成功,下次再见")
    logout_user()
    return redirect(url_for('auth.login'))


