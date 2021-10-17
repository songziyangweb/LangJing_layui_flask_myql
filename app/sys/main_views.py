from flask import render_template, request, jsonify, json
from . import sys
from ..models import User, Sensor, Device
from datetime import datetime
from app import db
import hashlib


# @sys.route('/user/index')
# def index():
#     return render_template('/user/index.html')




# @sys.route('/user/form')
# def form():
#     id = request.args.get('id', type=int)
#     if not id:
#         model = User.User()
#         model.id = 0
#         model.realname = ''
#         model.username = ''
#         model.sex = '女'
#     else:
#         model = User.User.query.filter(User.User.id == id).first()
#     return render_template('/user/form.html', model=model)
#
#
# @sys.route('/user/save', methods=['POST'])
# def save():
#     data = request.get_json()
#     print(data)
#     id = data['id']
#     realname = data['realname']
#     username = data['username']
#     print(realname, username, id)
#     if id == '0':
#         user = User.User()
#         user.username = username
#         user.realname = realname
#         user.sex = data['sex']
#         user.create_date = datetime.now()
#         md = hashlib.md5()
#         md.update('123456'.encode('utf-8'))
#         user.pwd = md.hexdigest()
#     else:
#         user = User.User.query.filter(User.User.id == id).first()
#         user.username = username
#         user.realname = realname
#         user.sex = data['sex']
#     try:
#         db.session.add(user)
#         db.session.commit()
#         return jsonify({'code': 0, 'msg': '保存成功'})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'code': -1, 'msg': '保存失败' + str(e)})
#
#
# @sys.route('/user/del', methods=['POST'])
# def delete():
#     data = request.get_json()
#     print(data['id'])
#     user = User.User.query.filter(User.User.id == data['id']).first()
#     try:
#         if user:
#             db.session.delete(user)
#             db.session.commit()
#             return jsonify({'code': 0, 'msg': '删除成功'})
#         else:
#             return jsonify({'code': 0, 'msg': '该用户不存在'})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'code': -1, 'msg': '删除失败：' + str(e)})
#
#
# def delete_batch():
#     data = request.get_json()
#     print(data['id'])
#
#
# @sys.route('/user/list', methods=['GET', 'POST'])
# def list():  # 用户查询功能
#     if request.method == 'GET':
#         page = request.args.get('page', type=int)
#         limit = request.args.get('limit', type=int)
#     else:
#         page = request.form.get('page', type=int)
#         limit = request.form.get('limit', type=int)
#     print(page)
#     print(limit)
#     if not page:
#         page = 1
#     if not limit:
#         limit = 10
#     realname = request.form.get('realname')
#     username = request.form.get('username')
#     print(realname)
#     print(username)
#     if not realname:
#         realname = ''
#     if not username:
#         username = ''
#
#     query = User.User.query
#     if username != '':
#         # query = query.filter_by(username=username)
#         # 模糊查询的写法
#         query = query.filter(User.User.username.like('%{username}%'.format(username=username)))
#     if realname != '':
#         # query = query.filter_by(realname=realname)
#         query = query.filter(User.User.realname.like('%{realname}%'.format(realname=realname)))
#     # users = query.all()
#     count = query.count()
#     print(count)
#     pagination = query.paginate(page, per_page=limit, error_out=False)
#     users = pagination.items
#     # users = User.User.query.all()
#     print(users)
#     data = [user.to_json() for user in users]
#     print(type(data))
#     return jsonify({'code': 0, 'msg': '请求成功', 'count': count, 'data': data})
