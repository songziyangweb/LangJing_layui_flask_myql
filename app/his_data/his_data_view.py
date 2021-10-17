from flask import render_template, request, jsonify
from app import db
from app.models.Device import Device, Sensor
from app.models.Sensor import SensorParamData, SensorParam
from app.his_data import his


@his.route('/his/index', methods=['GET', 'POST'])
def index():
    # 获取设备列表
    devices = Device.query.all()
    print(devices)
    return render_template("/his/index.html", devices=devices)


# 获取设备列表
@his.route('/his/devicelist', methods=['GET', 'POST'])
def device_list():
    return jsonify({'code': 0, 'msg': 'ok'})


@his.route('/his/sensor_list', methods=['GET', 'POST'])
def sensor_list():
    device_id = request.form['device_id']

    print(device_id);

    sensors = Sensor.query.filter(Sensor.device_id == device_id).order_by('sort_code').all()
    print(sensors)
    fields = []
    index = {
        'type': 'numbers',
        'title': '序号',
        'fixed': 'left'
    };
    fields.append(index)

    upload_date = {
        'field': 'upload_date',
        'title': '上报时间',
        'fixed': 'left',
        'width': '200'
    };
    fields.append(upload_date)

    for sensor in sensors:
        field = {
            'field': sensor.field_name,
            'title': sensor.sensor_name
        }
        fields.append(field)

    return jsonify({'code': 0, 'msg': 'ok', 'data': fields})


# 查询返回数据
@his.route('/his/search', methods=['GET', 'POST'])
def search():
    sql = "select * from t_5"
    data = db.session.execute(sql).fetchall()
    print(type(data))  # list
    print(type(data[0]))  # RowProxy
    d = dict(data[0].items())
    print(d)
    list = [dict(dt.items()) for dt in data]
    print(list)
    return jsonify({'code': 0, 'msg': 'ok', 'data': list})
