from flask import render_template, request, jsonify
from ..models import Device, User, Sensor
from . import device
from datetime import datetime
from app import db


@device.route('/device/index')
def index():
    return render_template('/device/index.html')


@device.route('/device/list', methods=['GET', 'POST'])
def list():
    if request.method == 'GET':
        page = request.args.get('page', type=int)
        limit = request.args.get('limit', type=int)
    else:
        page = request.form.get('page', type=int)
        limit = request.form.get('limit', type=int)

    if not page:
        page = 1
    if not limit:
        limit = 10
    devicename = request.form.get('devicename')

    if not devicename:
        devicename = ''

    query = Device.Device.query
    if devicename != '':
        # query = query.filter_by(username=username)
        # 模糊查询的写法
        query = query.filter(Device.Device.device_name.like('%{devicename}%'.format(devicename=devicename)))

    # users = query.all()
    count = query.count()

    pagination = query.paginate(page, per_page=limit, error_out=False)
    devices = pagination.items
    # users = User.User.query.all()
    data = [device.to_json() for device in devices]
    print(type(data))
    return jsonify({'code': 0, 'msg': '请求成功', 'count': count, 'data': data})


@device.route('/device/form')
def form():
    id = request.args.get('id', type=int)
    if not id:  # id为空
        model = Device.Device()
        model.id = 0
        model.device_name = ''
        model.site_code = ''
        model.device_code = ''
        model.address = ''
        model.sample_period = 60
        model.dtu_id = ''
    else:
        model = Device.Device.query.filter(Device.Device.id == id).first()
    return render_template('/device/form.html', model=model)


@device.route('/device/save', methods=['POST'])
def save():
    data = request.get_json()
    print(data)
    id = data['id']
    if id == '0':
        device = Device.Device()
        device.device_name = data['device_name']
        device.site_code = data['site_code']
        device.device_code = data['device_code']
        device.create_date = datetime.now()
        device.dtu_id = data['dtu_id']
        device.sample_period = data['sample_period']
        device.address = data['address']

    else:
        device = Device.Device.query.filter(Device.Device.id == id).first()
        device.device_name = data['device_name']
        device.site_code = data['site_code']
        device.device_code = data['device_code']
        device.create_date = datetime.now()
        device.dtu_id = data['dtu_id']
        device.sample_period = data['sample_period']
        device.address = data['address']
    try:
        db.session.add(device)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '保存成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': -1, 'msg': '保存失败' + str(e)})


@device.route('/device/del', methods=['POST'])
def delete():
    data = request.get_json()
    print(data['id'])
    device = Device.Device.query.filter(Device.Device.id == data['id']).first()
    try:
        if device:
            db.session.delete(device)

            db.session.commit()
            return jsonify({'code': 0, 'msg': '删除成功'})
        else:
            return jsonify({'code': 0, 'msg': '该用户不存在'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': -1, 'msg': '删除失败：' + str(e)})


@device.route('/device/set_sensor')
def sensor_form():
    device_id = request.args.get('id')

    return render_template('/device/set_sensor.html', device_id=device_id)


@device.route('/device/sensor_list', methods=['POST', 'GET'])
def get_sensor_list():
    device_id = request.args.get('id')
    print(device_id)
    # 查询出所有的传感器
    sensors = Sensor.SensorParam.query.all()
    # 查询出所有已经选中的传感器参数
    # selSensors = Device.Sensor.query.filter(Device.Sensor.device_id==device_id).all()
    # 使用一对多关联规则
    device = Device.Device.query.filter(Device.Device.id == device_id).first()
    selSensors = device.sensors
    print(selSensors)
    for sensor in sensors:
        flag = False
        for selsensor in selSensors:
            if selsensor.field_name == sensor.field_name:
                flag = True
        sensor.checked = flag

    data = [sensor.to_json() for sensor in sensors]
    print(type(data))
    print(len(data))
    print(data)
    return jsonify({'code': 0, 'msg': '请求成功', 'data': data})


@device.route('/device/set_sensor', methods=['POST', 'GET'])
def set_sensor():
    try:
        data = request.get_json()
        device_id = data['device_id']
        sensors = data['data']
        # 先删除原有数据
        delSensors = Device.Sensor.query.filter(Device.Sensor.device_id == int(device_id)).all()
        print(delSensors)
        if len(delSensors) > 0:
            for sensor in delSensors:
                db.session.delete(sensor)
            db.session.commit()
        print(sensors)
        for sensor in sensors:
            print(sensor)
            new_sensor = Device.Sensor()
            new_sensor.device_id = int(device_id)
            new_sensor.data_type = sensor['data_type']
            new_sensor.icon = sensor['icon']
            new_sensor.unit = sensor['unit']
            new_sensor.decimal_digit = sensor['decimal_digit']
            new_sensor.field_name = sensor['field_name']
            new_sensor.sort_code = sensor['sort_code']
            new_sensor.sensor_type = sensor['sensor_type']
            new_sensor.sensor_name = sensor['sensor_name']
            new_sensor.min_value = sensor['min_value']
            new_sensor.max_value = sensor['max_value']
            db.session.add(new_sensor)
            db.session.commit()
        return jsonify({'code': 0, 'msg': '保存成功'})
    except Exception as e:
        print(str(e))
        db.session.rollback()

        return jsonify({'code': -1, 'msg': '保存错误' + str(e)})


@device.route('/device/create_table', methods=['POST'])
def create_table():
    device_id = request.get_json()['id']
    device = Device.Device.query.filter(Device.Device.id == device_id).first()
    # 取出传感器内容
    sensors = device.sensors
    table_name = 't_' + str(device_id)
    # 建表语句
    sql = "create table `" + table_name + "` (" + \
          "`id` bigint(0) not null auto_increment," + \
          "`upload_date` datetime(0) not null,"
    for sensor in device.sensors:
        sql += "`" + sensor.field_name + "` " + sensor.data_type + " null default null,"
        # "`icon` decimal(10,2) null default null," + \
    sql += "primary key(`id`) using btree" + \
           ")"
    print(sql)
    try:
        db.session.execute(sql)
        return jsonify({'code': 0, 'msg': '建表成功'})
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({'code': -1, 'msg': '建表错误' + str(e)})
