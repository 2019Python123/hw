import os
from datetime import timedelta
import redis

basedir = os.path.abspath(os.path.dirname(__file__))  # 数据库基本路径
basedir_ = os.path.dirname(__file__)  # 数据库基本路径


class BaseConfig:
    """
    配置基类
    SECRET_KEY 会话密钥
    SQLALCHEMY_COMMIT_ON_TEARDOWN 是否自动提交数据库的会话
    FLASKY_SENDER 发送的邮箱
    FLASKY_ADMIN flask程序的管理员账号
    @staticmethod
    def init_app(self,app):
        pass
    用户初始化app
    config['development'].init_app(app)
    """
    # host='0.0.0.0'
    # port=5000
    SECRET_KEY = os.getenv('SECRET_KEY', b'_5#y2L"F4Q8z\n\xec]/')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_SENDER = 'FLASKY ADMIN <m17670415973@163.com>'
    FLASKY_ADMIN = os.getenv('FLASKY_ADMIN', 'm17670415973@163.com')
    FLASK_ADMIN_SWATCH = 'spacelab'
    # SESSION_TYPE = 'redis'
    # SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379', password='123456')
    REDIS_URL = 'redis://:123456@localhost:6379/0'
    HOME_WORD_PATH = os.path.join(basedir_,'/application/static/homeworks')
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    MAIL_SERVER = 'smtp.163.com'
    MAIL_USERNAME = 'm17670415973@163.com'
    MAIL_PASSWORD = 'BIDCAXBQWVWNWHRN'
    MAIL_USE_TLS = True
    MAIL_PORT = 25
    UPLOAD_FOLDER = basedir + "//application//static//self_images"
    MAX_SEARCH_RESULTS = 100
    ARTISAN_POSTS_PER_PAGE = 10

    @staticmethod
    def init_app(app) -> object:
        pass


class DevelopmentConfig(BaseConfig):
    """
    开发阶段的配置类，继承配置基类
    DEBUG = True 开启debug
    SQLALCHEMY_DATABASE_URI 定义数据库路径
    """
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/bookhomework_dev'


class TestingConfig(BaseConfig):
    """
    测试阶段的配置类，继承配置基类
    TESTING = True 开启测试模式
    SQLALCHEMY_DATABASE_URI 定义数据库路径
    """
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/bookhomework_test'


class ProductionConfig(BaseConfig):
    """
    SQLALCHEMY_DATABASE_URI 定义数据库路径
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/bookhomework'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
