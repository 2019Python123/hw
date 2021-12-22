from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flaskext.markdown import Markdown
from config import config
from flask_admin import Admin
from application.admin.views import PostsView,ExitView,UserCoreView,UserLogoutView,UserView,CreateHomeWorkView,ReleaseHomeWorkView
from application.admin.model_view import MessageView,UsersView,HomeWork_AuthorView,PostView,SpeciesView,Submit_LogView,HomeWork_UserView,RoleView,HomeWorkView
from flask_babelex import Babel
from flask_redis import  FlaskRedis
from flask_socketio import SocketIO
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib import rediscli
from redis import Redis

import os.path as op
babel = Babel()
redis = FlaskRedis()

admin = Admin(name=u'后台管理系统',template_mode='bootstrap3')
db = SQLAlchemy()
socket = SocketIO(logger=True, engineio_logger=True)
email = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = '/auth/login'


def app_factory(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    Markdown(app)
    socket.init_app(app)
    db.init_app(app)
    email.init_app(app)
    redis.init_app(app)
    babel.init_app(app)
    global admin
    admin.init_app(app)
    login_manager.init_app(app)
    register_blueprints(app)
    add_model_views()
    add_views()

    return app


def add_model_views():
    from application.models import User,Message,Species,Role,Post,Homework,HomeWork_User,Submit_Log,HomeWork_Author
    admin.add_view(UsersView(User,db.session,name='用户表'))
    admin.add_view(PostView(Post,db.session,name='文章表'))
    admin.add_view(Submit_LogView(Submit_Log,db.session,name='作业提交记录'))
    admin.add_view(RoleView(Role,db.session,name='角色表'))
    admin.add_view(HomeWorkView(Homework,db.session,name='作业表',category='作业'))
    admin.add_view(HomeWork_UserView(HomeWork_User,db.session,name='作业布置记录',category='作业'))
    admin.add_view(HomeWork_UserView(HomeWork_Author,db.session,name='创建作业记录',category='作业'))
    admin.add_view(SpeciesView(Species,db.session,name='标签表'))
    admin.add_view(MessageView(Message,db.session,name='消息'))


def add_views():
    admin.add_view(PostsView(name='博客'))
    admin.add_view(CreateHomeWorkView(name='新建作业',category="作业"))
    admin.add_view(ReleaseHomeWorkView(name='布置作业',category="作业"))
    path = op.join(op.dirname(__file__), 'static')
    admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
    admin.add_view(UserCoreView(name='个人中心',category="管理员"))
    admin.add_view(UserLogoutView(name='退出登录',category='管理员'))
    admin.add_view(ExitView(name='返回用户端',category='管理员'))


def register_blueprints(app):
    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp,url_prefix='/auth')
    from .admin import admin_bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    from .blog import blog as blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')
    from .main import main as main_bp
    app.register_blueprint(main_bp)
    from .ajax import ajax as ajax_bp
    app.register_blueprint(ajax_bp,url_prefix='/ajax')


