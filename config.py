import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Flask密钥和Session等相关
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Water102'
    # ？
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 邮件相关
    FLASK_MAIL_SUBJECT_PREFIX = '[Flask]'
    FLASK_MAIL_SENDER = 'DB.Jin<jindabing@qq.com>'
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
    # 表单加密
    CSRF_ENABLED = True
    # 设置session过期时间
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'stmp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #                         'sqlite:///' + os.path.join(basedir,"data-dev.sqlite")
    # 数据库配置
    # USERNAME = 'root'
    # PASSWORD = 'water102'
    # HOST = '182.92.217.4'
    # PORT = '3306'
    # DATABASE = 'langjing'

    USERNAME = 'root'
    PASSWORD = '123456'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'student'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
        USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 动态跟踪修改设置，如果未设置会弹出警告
    SQLALCHEMY_ECHO = False  # 查询时会显示原始的sql语句


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
