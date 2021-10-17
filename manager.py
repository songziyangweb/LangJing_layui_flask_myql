'''
程序控制
'''
import os
from app import create_app, db
from flask_script import Manager, Shell
from flask import g, render_template
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Sensor, Device
from app.utils.CustomJSONEncoder import CustomJSONEncoder

app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)  # 数据库与app建立绑定

app.json_encoder = CustomJSONEncoder


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('errors/404.html'),404


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))  # 添加迁移命令集 到脚本命令
manager.add_command('db', MigrateCommand)  # 添加迁移命令集 到脚本命令


@manager.command
def myprint():
    print('hello world')


if __name__ == '__main__':
    manager.run(debug=True)
