from threading import Thread

from flask_login import login_required,current_user
from flask import session,request,jsonify,url_for,render_template,make_response,send_from_directory
from . import ajax
from application.helper import *
from application import db
import json
from application import email
from flask_mail import Message
# from application.send_email import send_async_email
# from application.send_email import send_email
from application.models import *
from sqlalchemy import or_,and_


@ajax.route("/get_captcha",methods=['GET'])
def get_captcha():
    content = {}
    img_src, yzm = get_file("application/static/captcha")
    print("ajax"+yzm)
    session['yzm'] = yzm
    content['img_src'] = "/static/"+img_src
    return jsonify({'code':200,'msg':content})


@ajax.route("/upload_img",methods=['POST'])
@login_required
def upload_mg():
    if request.method == 'POST':
        file = request.files['file']
        data = img_to_base64(file.read(),file.name.split(".")[-1])
        current_user.img_data = data
        db.session.add(current_user)
        db.session.commit()
        return jsonify({'code':200,'msg':{'data':data}})


@ajax.route("/modify_formation",methods=['POST'])
@login_required
def modify_formation():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    if data['yzm'].lower() == session['yzm'].lower() :
        current_user.name = data['name'] if data['name']!='' else current_user.name
        current_user.sex = data['sex'] if data['sex'] != '' else current_user.sex
        current_user.zhuanye = data['zy'] if data['zy']!= '' else current_user.zhuanye
        current_user.about_me = data['zym'] if data['zym']!='' else current_user.about_me
        db.session.add(current_user)
        db.session.commit()
        return jsonify({'code':200,'msg':'更新信息成功'})
    else:
        return jsonify({'code': 500, 'msg': '更新信息失败'})


@ajax.route("/get_email_yzm",methods=['POST'])
@login_required
def get_yzm():
    recipe = request.get_data(as_text=True)
    recipe = json.loads(recipe)
    print(recipe)

    yzm = randint(1000, 9999)
    session['yzm'] = str(yzm)
    body = '您的验证码是: <h3>' + str(yzm) + '</h3>'
    if current_user.email is None:
        msg = Message('绑定邮箱认证', sender=current_app.config['MAIL_USERNAME'], recipients=[recipe['email'], ])
        msg.body = body
        email.send(msg)
    else:
        msg = Message('绑定邮箱认证', sender=current_app.config['MAIL_USERNAME'], recipients=[current_user.email, ])
        msg.body = body
        email.send(msg)
    return jsonify({'code':200,'msg':'发送验证码成功，请及时进行验证'})


@ajax.route("/modify_email",methods=['POST'])
@login_required
def modify_email():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    if data['yzm'].lower() == session['yzm'].lower():
        current_user.email = data['email']
        db.session.add(current_user)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '更新email成功'})
    else:
        return jsonify({'code': 500, 'msg': '更新email失败'})


@ajax.route("/modify_passwd",methods=['POST'])
@login_required
def modify_passwd():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    print(data)
    if data['yzm'].lower() == session['yzm'].lower():
        current_user.password = data['passwd']
        db.session.add(current_user)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '更新密码成功'})
    else:
        return jsonify({'code': 500, 'msg': '更新密码失败'})


@ajax.route("/get_posts",methods=['POST'])
@login_required
def get_posts():
    data_json = json.loads(request.get_data(as_text=True))
    page = int(data_json['page'])
    pagination = Post.query.filter_by(author_id=current_user.id).order_by(Post.timestmp.desc()).paginate(page=page,per_page=10)
    posts = pagination.items
    species = Species.query.all()
    data = render_template("_posts.html",posts=posts,pagination=pagination,show_collect=False,species=species)
    return jsonify({'code':200,'msg':{'data':data}})


@ajax.route("/get_posts/species",methods=['POST'])
@login_required
def get_posts_species():
    data_json = json.loads(request.get_data(as_text=True))
    page = int(data_json['page'])
    sp = Species.query.filter_by(name=data_json['sp_id']).first()
    pagination = Post.query.filter_by(author_id=current_user.id,species_id=sp.id).order_by(Post.timestmp.desc()).paginate(page=page,per_page=10)
    posts = pagination.items
    species = Species.query.all()
    data = render_template("_posts.html",posts=posts,pagination=pagination,show_collect=False,species=species)
    return jsonify({'code':200,'msg':{'data':data}})


@ajax.route("/get_collect_posts",methods=['POST'])
@login_required
def get_collect_posts():
    data_json = json.loads(request.get_data(as_text=True))
    page = int(data_json['page'])
    pagination = Collect.query.filter_by(collect_user_id=current_user.id).order_by(Collect.timestamp.desc()).paginate(page=page,per_page=10)
    collects = pagination.items
    posts = []
    for collect in collects:
        post = Post.query.filter_by(id=collect.collect_post_id).first()
        posts.append(post)
    species = Species.query.all()
    data = render_template("_posts.html",posts=posts,pagination=pagination,show_collect=True,collects=collects,species=species)
    return jsonify({'code':200,'msg':{'data':data}})


@ajax.route("/get_works",methods=['POST'])
@login_required
def get_works():
    data_json = json.loads(request.get_data(as_text=True))
    page = int(data_json['page'])
    pagination = HomeWork_User.query.filter_by(owner_id=current_user.id).order_by(HomeWork_User.timestmp.desc()).paginate(
        page=page, per_page=10)
    posts = []
    for post in pagination.items:
        post_ = Homework.query.filter_by(id=post.homework_id).first()
        posts.append(post_)
    species = Species.query.all()
    data = render_template("blog/works.html",posts=posts,pagination=pagination,h_us=pagination.items,species=species)
    return jsonify({'code':200,'msg':{'data':data}})


@ajax.route("/get_works_species",methods=['POST'])
@login_required
def get_works_species():
    data_json = json.loads(request.get_data(as_text=True))
    page = int(data_json['page'])
    pagination = HomeWork_User.query.filter_by(owner_id=current_user.id).order_by(HomeWork_User.timestmp.desc()).paginate(
        page=page, per_page=10)
    posts = []
    print(data_json)
    for post in pagination.items:
        post_ = Homework.query.filter_by(id=post.homework_id,species_name=data_json['sp_id']).first()
        if post_ is not None:
            posts.append(post_)
    print(posts)
    species = Species.query.all()
    data = render_template("blog/works.html",posts=posts,pagination=pagination,h_us=pagination.items,species=species)
    return jsonify({'code':200,'msg':{'data':data}})


@ajax.route("/get_messages",methods=['GET'])
@login_required
def get_messages():
    msgs = Message.query.filter_by(accept_id=current_user.id).all()
    users = []
    for msg in msgs:
        user = User.query.filter_by(id=msg.sender_id).first()
        users.append(user)
    html = render_template("messages.html",messages=msgs,users=users)
    return jsonify({'data':html})


@ajax.route("/is_read",methods=['POST'])
@login_required
def is_read():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    msg = Message.query.filter_by(id=data['id']).first()
    msg.is_read = True
    db.session.add(msg)
    db.session.commit()
    mgs = Message.query.filter_by(accept_id=current_user.id,is_read=False).all()
    return jsonify({'code':200,'id':'msg_'+str(data['id']),'count':len(mgs)})


@ajax.route("/del_msg",methods=['POST'])
@login_required
def del_msg():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    msg = Message.query.filter_by(id=data['id']).first()
    db.session.delete(msg)
    db.session.commit()
    return jsonify({'code':200,'id':'msg_'+str(data['id'])})


@ajax.route('/collect_post',methods=['POST'])
@login_required
def collect_post():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    print(data)
    collect = Collect(collect_post_id=data['id'],collect_user_id=current_user.id)
    db.session.add(collect)
    db.session.commit()
    return jsonify({'code':200,'msg':'收藏成功','id':data['id']})


@ajax.route('/un_collect_post',methods=['POST'])
@login_required
def un_collect_post():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    print(data)
    collect = Collect.query.filter_by(collect_post_id=data['id'],collect_user_id=current_user.id).first()
    print(collect)
    db.session.delete(collect)
    db.session.commit()
    return jsonify({'code':200,'msg':'取消收藏成功','id':data['id']})


@ajax.route("/download_file",methods=['POST'])
@login_required
def down_file():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    path = ''
    ds = session['system_file_path'].split('\\')
    for paths in range(len(ds)):
        if paths < len(ds):
            path += ds[paths]+'\\'
        else:
            break;
    print(path)
    send_from_directory(directory=path, filename=data['file'], as_attachment=True)
    # 'data': send_from_directory(directory=path, filename=data['file'], as_attachment=True)
    return jsonify({'code':200})


@ajax.route('/submit_homework',methods=['POST'])
@login_required
def submit_homework():
    data = json.loads(request.get_data(as_text=True))
    if data['flag'] == 'blog':
        url = data['url']
        h_u = Submit_Log.query.filter_by(submiter_id=current_user.id,homework_id=data['id'],submiter_name=current_user.name).first()
        if h_u is None:
            submit = Submit_Log(submiter_id=current_user.id,answer=url,homework_id=data['id'],submiter_name=current_user.name)
            h_u_ = HomeWork_User.query.filter_by(homework_id=submit.homework_id,owner_id=current_user.id).first()
            if h_u_:
                h_u_.is_complete = True
                db.session.add(h_u_)
            db.session.add(submit)
            db.session.commit()
        else:
            h_u.answer = url
            db.session.add(h_u)
            db.session.commit()
    return jsonify({'code':200})


@ajax.route('/submit_homework_file',methods=['POST'])
@login_required
def submit_homework_file():
    file = request.files['file']
    print(file.filename)
    import os.path as op
    print(os.path.dirname(__file__))
    path = ''
    ops = os.path.dirname(__file__).split("\\")
    for p in range(len(ops)):
        if p < len(ops) -1:
            path += ops[p]+'\\'
        else:
            pass

    path += 'static\\homeworks\\'
    file.save(path+file.filename)
    return jsonify({'code':200,'path':path+file.filename})


@ajax.route('/search',methods=['POST'])
@login_required
def search():
    data = json.loads(request.get_data(as_text=True))
    data_ = data
    print(data)
    if data['type'] == 'work':
        page = int(data['page'])
        pagination = HomeWork_User.query.filter_by(owner_id=current_user.id).order_by(
            HomeWork_User.timestmp.desc()).paginate(
            page=page, per_page=10)
        posts = []
        for post in pagination.items:
            post_ = Homework.query.filter(or_(Homework.body.like("%"+(data['content'])+"%"),
                                             Homework.title.like("%"+(data['content'])+"%"))).first()
            posts.append(post_)
        species = Species.query.all()
        data = render_template("main/ajax_works.html", posts=posts, pagination=pagination, h_us=pagination.items,
                               species=species)
        return jsonify({'code': 200, 'msg': {'data': data,'type':data_['type']}})
    elif data['type'] == 'post':
        page = int(data['page'])
        pagination = Post.query.filter(
            or_(Post.title.like("%"+(data['content'])+"%"),
                Post.body.like("%"+(data['content'])+"%"))).order_by(Post.timestmp.desc()).paginate(page=page,
                                                                                                  per_page=10)
        posts = pagination.items
        species = Species.query.all()
        data = render_template("main/ajax_posts.html", posts=posts, pagination=pagination, species=species)
        return jsonify({'code': 200, 'msg': {'data': data,'type':data_['type']}})
    else:
        pass


@ajax.route('/search_self',methods=['POST'])
@login_required
def search_self():
    data = json.loads(request.get_data(as_text=True))
    data_ = data
    print(data)
    if data['type'] == 'work':
        page = int(data['page'])
        pagination = HomeWork_User.query.filter_by(owner_id=current_user.id).order_by(
            HomeWork_User.timestmp.desc()).paginate(
            page=page, per_page=10)
        posts = []
        for post in pagination.items:
            post_ = Homework.query.filter(or_(Homework.body.like("%"+(data['content'])+"%"),
                                             Homework.title.like("%"+(data['content'])+"%"))).first()
            posts.append(post_)
        species = Species.query.all()
        data = render_template("blog/works.html", posts=posts, pagination=pagination, h_us=pagination.items,
                               species=species)
        return jsonify({'code': 200, 'msg': {'data': data,'type':data_['type']}})
    elif data['type'] == 'post':
        page = int(data['page'])
        pagination = Post.query.filter(
            or_(Post.title.like("%"+(data['content'])+"%"),
                Post.body.like("%"+(data['content'])+"%"))).order_by(Post.timestmp.desc()).paginate(page=page,
                                                                                                  per_page=10)
        posts = pagination.items
        species = Species.query.all()
        data = render_template("_posts.html", posts=posts, pagination=pagination,show_collect=False, species=species)
        return jsonify({'code': 200, 'msg': {'data': data,'type':data_['type']}})
    else:
        pass