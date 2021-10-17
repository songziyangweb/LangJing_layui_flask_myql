from flask import render_template, jsonify, request
from app import db
from app.models.Device import Device, DeviceCmd, Sensor, DeviceLog
from app.models.Sensor import SensorParam, SensorParamData
from ..device_monitor import monitor


@monitor.route('/monitor/index', methods=['POST', 'GET'])
def index():
    return render_template('/monitor/index.html')


# 表头元素
def sensor_list():
    device = Device.query.first()
    sensors = Sensor.query.filter(Sensor.device_id == device.id).order_by('sort_code').all()
    print(sensors)
    fields = []
    index = {
        'type': 'numbers',
        'title':'序号',
        'fixed':'left'
    };
    fields.append(index)
    device = {
        'field': 'device_name',
        'title': '设备名称',
        'fixed':'left',
        'width':'150'
    };
    fields.append(device)
    upload_date = {
        'field': 'last_upload_date',
        'title': '上报时间',
        'fixed':'left',
        'width':'200'
    };
    fields.append(upload_date)
    is_online = {
        'field':'is_online',
        'title':'在线状态',
        'fixed':'left',
        'templet':'#onlineTp'
    }
    fields.append(is_online)
    for sensor in sensors:
        field = {
            'field': sensor.field_name,
            'title': sensor.sensor_name
        }
        fields.append(field)
    return fields


# 带实时数据的设备列表
@monitor.route('/monitor/list_with_data', methods=['POST', 'GET'])
def list_with_data():
    devicename = request.form.get('devicename')

    if not devicename:
        devicename = ''

    query = Device.query
    if devicename != '':
        # query = query.filter_by(username=username)
        # 模糊查询的写法
        query = query.filter(Device.device_name.like('%{devicename}%'.format(devicename=devicename)))
    devices = query.all()
    data = []
    for device in devices:
        dict = device.to_json()
        print(dict)
        last_data = dict['last_data']
        # 拆分数据
        strlist = last_data.split(',')
        for str in strlist:
            item = str.split(':')
            dict[item[0]] = float(item[1])
        print(dict)
        data.append(dict)
    # data = [device.to_json() for device in devices]
    print(type(data))
    return jsonify({'code': 0, 'msg': '请求成功', 'data': data})


@monitor.route('/monitor/list', methods=['POST', 'GET'])
def list():
    devicename = request.form.get('devicename')

    if not devicename:
        devicename = ''

    query = Device.query
    if devicename != '':
        # query = query.filter_by(username=username)
        # 模糊查询的写法
        query = query.filter(Device.device_name.like('%{devicename}%'.format(devicename=devicename)))
    devices = query.all()

    data = [device.to_json() for device in devices]
    print(type(data))
    return jsonify({'code': 0, 'msg': '请求成功', 'data': data})


@monitor.route('/monitor/dataview', methods=['POST', 'GET'])
def data_view():
    fields = sensor_list()
    return render_template('/monitor/dataview.html',cols=fields)


@monitor.route('/monitor/get_realdatda', methods=['POST', 'GET'])
def get_realdata():
    devicename = request.form.get('devicename')
    if not devicename:
        devicename = ''

    query = Device.query
    if devicename != '':
        # query = query.filter_by(username=username)
        # 模糊查询的写法
        query = query.filter(Device.device_name.like('%{devicename}%'.format(devicename=devicename)))
    devices = query.all()
    data = [device.to_json() for device in devices]
    return jsonify({'code': 0, 'msg': '获取成功', 'data': data})


@monitor.route('/monitor/cmdview', methods=['POST', 'GET'])
def cmd_view():
    return render_template('/monitor/cmdview.html')


@monitor.route('/monitor/logview', methods=['POST', 'GET'])
def log_view():
    return render_template('/monitor/logview.html')
