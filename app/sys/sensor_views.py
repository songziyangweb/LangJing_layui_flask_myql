from flask import render_template, request, jsonify
from app import db
from . import sys
from ..models import Sensor


@sys.route('/sensor/index')
def sensor_index():
    return render_template('/sensor/index.html')


@sys.route('/sensor/list', methods=['GET', 'POST'])
def sensor_list():
    if request.method == 'GET':
        page = request.args.get('page', type=int)
        limit = request.args.get('limit', type=int)
    else:
        page = request.form.get('page', type=int)
        limit = request.form.get('limit', type=int)
    print(page)
    print(limit)
    if not page:
        page = 1
    if not limit:
        limit = 10
    sensor_name = request.form.get('sensor_name')
    field_name = request.form.get('field_name')
    print(sensor_name)
    print(field_name)
    if not sensor_name:
        sensorname = ''
    if not field_name:
        fieldname = ''

    query = Sensor.SensorParam.query
    if sensor_name != '':
        # query = query.filter_by(username=username)
        # 模糊查询的写法
        query = query.filter(Sensor.SensorParam.sensor_name.like('%{sensor_name}%'.format(sensor_name=sensor_name)))
    if field_name != '':
        # query = query.filter_by(realname=realname)
        query = query.filter(Sensor.SensorParam.field_name.like('%{field_name}%'.format(field_name=field_name)))
    # users = query.all()
    count = query.count()
    print(count)
    pagination = query.paginate(page, per_page=limit, error_out=False)
    sensors = pagination.items
    # users = User.User.query.all()
    print(sensors)
    data = [sensor.to_json() for sensor in sensors]
    print(type(data))
    return jsonify({'code': 0, 'msg': '请求成功', 'count': count, 'data': data})


@sys.route('/sensor/form')  # 添加
def sensor_form():
    id = request.args.get('id', type=int)
    if not id:
        model = Sensor.SensorParam()
        model.id = 0
        print(model)

    else:
        model = Sensor.SensorParam.query.filter(Sensor.SensorParam.id == id).first()
        print(model)

    return render_template('/sensor/form.html', model=model)


@sys.route('/sensor/save', methods=['POST'])
def sensor_save():
    data = request.get_json()
    print(data)
    id = data['id']

    if id == '0':
        sensor = Sensor.SensorParam()
        sensor.sensor_name = data['sensor_name']
        sensor.field_name = data['field_name']
        sensor.data_type = data['data_type']
        sensor.decimal_digit = data['decimal_digit']
        sensor.unit = data['unit']
        sensor.max_value = data['max_value']
        sensor.min_value = data['min_value']
        sensor.sort_code = data['sort_code']
        sensor.sensor_type = data['sensor_type']

    else:
        sensor = Sensor.SensorParam.query.filter(Sensor.SensorParam.id == id).first()
        sensor.sensor_name = data['sensor_name']
        sensor.field_name = data['field_name']
        sensor.data_type = data['data_type']
        sensor.decimal_digit = int(data['decimal_digit'])
        sensor.unit = data['unit']
        sensor.max_value = data['max_value']
        sensor.min_value = data['min_value']
        sensor.sort_code = data['sort_code']
        sensor.sensor_type = data['sensor_type']
    try:
        db.session.add(sensor)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '保存成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': -1, 'msg': '保存失败' + str(e)})


@sys.route('/sensor/del', methods=['POST'])
def sensor_delete():
    data = request.get_json()
    print(data['id'])
    sensor = Sensor.SensorParam.query.filter(Sensor.SensorParam.id == data['id']).first()
    try:
        if sensor:
            db.session.delete(sensor)
            db.session.commit()
            return jsonify({'code': 0, 'msg': '删除成功'})
        else:
            return jsonify({'code': 0, 'msg': '该用户不存在'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': -1, 'msg': '删除失败：' + str(e)})
