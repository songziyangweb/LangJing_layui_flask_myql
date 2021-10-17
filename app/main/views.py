from flask import render_template, url_for, jsonify, request, json, redirect
from . import main
from app.models import User, Sensor, Device
from flask_login import login_user, logout_user, login_required, current_user
import hashlib
from app import db


# @main.app_errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
#
# @main.app_errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500


@main.route('/login', methods=['GET'])
def login():
    '''
    登陆页
    :return:
    '''

    return render_template('login.html')


@main.route('/dologin', methods=['POST'])
def dologin():
    data = request.get_json()
    print(data['username'])
    print(data['pwd'])

    user = User.User.query.filter_by(username=data.get('username')).first()
    if user is not None:
        md = hashlib.md5()
        md.update(data.get('pwd').encode('utf-8'))

        if user.pwd == md.hexdigest():
            login_user(user)
            return jsonify({'code': 0, 'msg': '登陆成功'})
        else:
            return jsonify({'code': -1, 'msg': '密码错误'})


    else:
        return jsonify({'code': -1, 'msg': '用户不存在'})

#


@main.route('/dologon', methods=['POST'])
def dologon():
    data = request.get_json()
    print(data['username'])
    username = data['username']
    pwd = data['pwd']
    id = data['id']
    sex = data['sex']
    realname = data['realname']

    user = User.User.query.filter_by(username=data.get('username')).first()  # 查找data在数据库中是否存在
    if user is None:
        md = hashlib.md5()
        md.update(data.get('pwd').encode('utf-8'))
        pwd = md.hexdigest()

        user_data = User.User(id=id, username=username, sex=sex, pwd=pwd, realname=realname)
        db.session.add(user_data)

        db.session.commit()
        return jsonify({'code': 0, 'msg': '注册成功'})
    else:
        return jsonify({'code': -1, 'msg': '用户已存在'})


@main.route('/logout')
def dologout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@main.route('/logon1', methods=['GET', 'POST'])
# @login_required
def logon1():
    return render_template('logon.html')

@main.route('/main_index',methods=['GET'])
def main_index():
    return render_template('main_index.html')
@main.route('/test', methods=['GET'])
def test():
    return 'test'
