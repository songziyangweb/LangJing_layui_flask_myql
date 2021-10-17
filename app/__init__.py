from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager


loginManager = LoginManager()
loginManager.session_protection = 'strong'
loginManager.login_view = 'main.login'

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    loginManager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .sys import sys as sys_blueprint
    app.register_blueprint(sys_blueprint)

    from .device import device as device_blueprint
    app.register_blueprint(device_blueprint)

    from .device_monitor import monitor as monitor_blueprint
    app.register_blueprint(monitor_blueprint)

    from .his_data import his as his_blueprint
    app.register_blueprint(his_blueprint)


    return app