from flask import current_app,url_for,redirect,flash

from application import db,login_manager,app_factory
from datetime import datetime
from pytz import timezone
from flask_login import AnonymousUserMixin,UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


from sqlalchemy.dialects.mysql import MEDIUMTEXT


cst_tz = timezone('Asia/Shanghai')


class Submit_Log(db.Model):
    """
    用户提交作业表
    """
    __tablename__ = 'submit_logs'
    id = db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    homework_id = db.Column(db.Integer,db.ForeignKey('homeworks.id'))
    submiter_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    submiter_name = db.Column(db.String(100))
    answer = db.Column(db.String(1000))
    timestmp = db.Column(db.DateTime, default=datetime.now(cst_tz))


class HomeWork_User(db.Model):
    """
    布置任务
    """
    __tablename__='homework_users'
    id = db.Column(db.Integer, primary_key=True,unique=True,nullable=False)
    homework_id = db.Column(db.Integer, db.ForeignKey('homeworks.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    owner_name = db.Column(db.String(100))
    publish_name = db.Column(db.String(100))
    is_complete = db.Column(db.Boolean,default=False)
    grade = db.Column(db.Integer)
    timestmp = db.Column(db.DateTime, default=datetime.now(cst_tz))


class Collect(db.Model):
    __tablename__ = 'collects'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True,unique=True,nullable=False)
    collect_post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True
    )
    collect_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    )
    timestamp = db.Column(db.DateTime, default=datetime.now(cst_tz))


class Message(db.Model):
    __tablename__='messages'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    body = db.Column(db.Text())
    sender_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    accept_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    is_read = db.Column(db.Boolean,default=False)
    timestmp = db.Column(db.DateTime, default=datetime.now(cst_tz))


class HomeWork_Author(db.Model):
    """
    布置任务
    """
    __tablename__='homework_authors'
    id = db.Column(db.Integer, primary_key=True,unique=True,nullable=False)
    homework_id = db.Column(db.Integer, db.ForeignKey('homeworks.id'))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author_name = db.Column(db.String(100))
    timestmp = db.Column(db.DateTime, default=datetime.now(cst_tz))


class LearningDirection(db.Model):
    __tablename__='learning_directions'
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column(db.String(255),nullable=False)
    timestmp = db.Column(db.DateTime,default=datetime.now(cst_tz))


# 程序权限
class Permission:
    # 关注别人的权限
    FOLLOW = 0x01
    # 评论权限
    COMMENT = 0x02
    # 写文章权限
    WRITE_ARTICLES = 0x04
    # 协住管理员权限
    MODERATE_COMMENTS = 0x08
    # 管理员权限
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__='roles'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    role_name = db.Column(db.String(255))
    # 默认注册后的角色，否则赋予其他角色
    default = db.Column(db.Boolean, default=False)
    # 权限值
    permission = db.Column(db.Integer)
    # 与users表关联
    users = db.relationship('User', backref='role', lazy='dynamic')
    timestmp = db.Column(db.DateTime,default=datetime.now(cst_tz))

    @staticmethod
    def insert_role():
        # 角色字典
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'For_words_user': (Permission.FOLLOW |
                               Permission.WRITE_ARTICLES, False),
            'For_write_user': (Permission.FOLLOW |
                               Permission.COMMENT, False),
            'For_follow_user': (Permission.COMMENT |
                                Permission.WRITE_ARTICLES, False),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        # 角色字典遍历
        for r in roles:
            # 查询是否有上面的角色字典里的角色
            role = Role.query.filter_by(role_name=r).first()
            # 如果没有
            if role is None:
                # 将角色字典的值填充数据库角色表新的一行记录
                role = Role(role_name=r)
            role.default = roles[r][1]
            role.permission = roles[r][0]
            # 将这个记录加到会话中
            db.session.add(role)
        # 向数据库提交会话
        db.session.commit()


class User(UserMixin,db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    # 学号+姓名
    name = db.Column(db.String(255),unique=True,nullable=False)
    passwd_hash = db.Column(db.String(255))
    email = db.Column(db.String(255),unique=True)
    img_data = db.Column(MEDIUMTEXT())
    sex = db.Column(db.String(10))
    # 19网络二班
    zhuanye = db.Column(db.String(100))
    about_me = db.Column(db.String(2000))
    timestmp = db.Column(db.DateTime,default=datetime.now(cst_tz))
    main_ = db.Column(db.String(255))
    fuxiu_= db.Column(db.String(255))
    homeworks = db.relationship('Submit_Log',backref='submiter',lazy='dynamic')
    posts = db.relationship('Post',backref='user',lazy='dynamic')
    homeworkers = db.relationship('HomeWork_Author',backref='author',lazy='dynamic')
    homework_ofs = db.relationship('HomeWork_User',backref='owner',lazy='dynamic')
    sender = db.relationship('Message', foreign_keys=[Message.sender_id],
                               backref=db.backref('sender', lazy='joined'), lazy='dynamic')
    accept_ = db.relationship('Message', foreign_keys=[Message.accept_id],
                               backref=db.backref('accept', lazy='joined'), lazy='dynamic')
    collect_posts = db.relationship(
        'Collect',
        foreign_keys=[Collect.collect_user_id],
        lazy='dynamic',
        cascade='all,delete-orphan'
    )


    # 初始化user对象
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role_id = Role.query.filter_by(id=6).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    # 将函数变成属性
    @property
    def password(self):
        return self.passwd_hash

    # 给password_hash赋值
    @password.setter
    def password(self, password):
        self.passwd_hash = generate_password_hash(password)

    # 定义函数用来检查密码
    def verify_password_hash(self, password):
        return check_password_hash(self.passwd_hash, password)


class Homework(db.Model):
    __tablename__='homeworks'
    id = db.Column(db.Integer, primary_key=True,unique=True,nullable=False)
    title = db.Column(db.String(1000),nullable=False)
    body = db.Column(db.Text(),nullable=False)
    # 对题目进行描述的字段
    describe = db.Column(db.Text())
    species_name = db.Column(db.String(255))
    # 所属 作业类型
    species_id = db.Column(db.Integer,db.ForeignKey('species.id'))
    author_name = db.Column(db.String(255))
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    # 炼气、筑基、旋照、融合、心动、灵寂、元婴、出窍、分神、合体、度劫、大乘、渡劫
    difficulty = db.Column(db.String(255))
    is_url = db.Column(db.Boolean,default=False)
    timestmp = db.Column(db.DateTime, default=datetime.now(cst_tz))
    homeworks = db.relationship('Submit_Log',backref='homework',lazy='dynamic')
    homework_logs = db.relationship('HomeWork_Author',backref='homework_log',lazy='dynamic')
    homework_oflogs = db.relationship('HomeWork_User',backref='homework_of',lazy='dynamic')



class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    title = db.Column(db.String(255))
    body = db.Column(db.Text())
    author_name = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    species_id = db.Column(db.Integer,db.ForeignKey('species.id'))
    users = db.relationship(
        'Collect',
        foreign_keys=[Collect.collect_post_id],
        lazy='dynamic',
        cascade='all,delete-orphan'
    )
    timestmp = db.Column(db.DateTime, default=datetime.now(cst_tz))





class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    name = db.Column(db.String(555),unique=True,nullable=False)
    homeworks = db.relationship('Homework',backref='species',lazy='dynamic')
    posts = db.relationship('Post',backref='post_species',lazy='dynamic')
    timestmp = db.Column(db.DateTime, default=datetime.now(cst_tz))






class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


# flask_login需要用户的id来管理用户登录的情况
@login_manager.user_loader
def load_user(user_id):
    return User.query.get_or_404(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("请你登录再使用本网站功能")
    return redirect(url_for('auth.login'))


login_manager.anonymous_user = AnonymousUser

if __name__ == '__main__':
    app_factory().app_context().push()
    db.drop_all()
