from application import app_factory
from flask import render_template,send_from_directory
from flask_script import Shell,Manager
from flask_migrate import Migrate,MigrateCommand
from application import db,socket,redis,admin
from application.fakerdata import *
from application.models import *
from flask_socketio import  send,emit
from markdown import markdown
from flask_login import current_user,login_required
from flask_socketio import join_room,leave_room
import json


# 实例化app
app = app_factory()

# 数据库迁移类的实例化对象
migrate = Migrate(app,db)
# 创建脚本管理类实例化对象
manager = Manager(app)
# 将数据库迁移命令添加到终端命令里
manager.add_command('db',MigrateCommand)


def make_shell_context():
    return dict(
        db=db,Role=Role,Species=Species,faker=faker
    )


command = manager.add_command('shell', Shell(make_context=make_shell_context))


@app.route("/socket")
def socket_ceshi():
    redis.set('id','{"mg":"[1,2,3,4,5]"}')
    return render_template("in.html")


@socket.on('query_msg')
def query_msg(data):
    print(data)
    msgs = Message.query.filter_by(accept_id=current_user.id,is_read=False).all()
    print(msgs)
    msg = ''
    if len(msgs) == 0:
        msg += '没有未读消息'
    else:
        for m in msgs:
            msg += m.body
    count = len(msgs)

    socket.emit('get_query_msg',{'msg':msg,'count':count},room=current_user.id)


@socket.on('msg')
def send_homework_msg(json_):
    data = json_
    message = '您有一份作业请签收！'
    if len(data['users']) >0:
        for user in data['users']:
            from application.models import Message
            msg = Message(accept_id=user,sender_id=int(data['sender']),body=message)
            db.session.add(msg)
            db.session.commit()
            msg_ = Message.query.filter_by(accept_id=user,sender_id=int(data['sender'])).order_by(Message.timestmp.desc()).first()
            user_ = User.query.filter_by(id=user).first()
            html = render_template("message.html", message=msg_,user=user_)
            socket.emit('accept_message', {'msg': message,'html':html}, room=user)


@socket.on('join')
@login_required
def joined_room():
    print('加入房间了')
    join_room(current_user.id)


@socket.on('leave')
@login_required
def leaved_room():
    print("离开房间了")
    leave_room(current_user.id)


@app.template_filter('md')
def markdown_to_html(txt):
    return markdown(txt, ['extra'])


@app.before_request
def before():
    from flask import request
    paths = request.path.split('/')
    if paths[1] == 'admin':
        if current_user.is_authenticated and current_user.role_id==6:
            pass
        else:
            return redirect(url_for('auth.login'))


@app.route("/download")
@login_required
def index():
    return send_from_directory(r"D:\\Files\\PycharmProjects\\bookHomeWork\\application\\static\\img\\",filename="admin_bg.jpeg",as_attachment=True)


if __name__ == '__main__':
    manager.run()









