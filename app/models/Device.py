from app import db
from datetime import datetime

class Device(db.Model):
    __tablename__ = 'device'
    id = db.Column(db.Integer,primary_key=True)
    device_name = db.Column(db.String(100),nullable=False)
    site_code = db.Column(db.String(10),nullable=False,index=True)
    device_code = db.Column(db.String(10),nullable=False,index=True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    address = db.Column(db.String(200))
    sample_period = db.Column(db.Integer,default=60) # 采样周期默认60秒
    dtu_id = db.Column(db.String(20),nullable=False,index=True)
    is_online = db.Column(db.Integer,default=0) # 上线状态,默认位0
    create_date = db.Column(db.DateTime,default=datetime.now)
    last_upload_date = db.Column(db.DateTime)
    last_data = db.Column(db.String(500)) # 最后接收到的数据

    sensors = db.relationship('Sensor',backref='Device')

    def to_json(self):
        return {
            'id':self.id,
            'device_name':self.device_name,
            'site_code':self.site_code,
            'device_code':self.device_code,
            'address':self.address,
            'sample_period':self.sample_period,
            'longitue':self.longitude,
            'latitude':self.latitude,
            'dtu_id':self.dtu_id,
            'is_online':self.is_online,
            'create_date':self.create_date.strftime('%Y-%m-%d %H:%M:%S'),
            'last_upload_date':self.last_upload_date.strftime('%Y-%m-%d %H:%M:%S'),
            'last_data':self.last_data
        }


class Sensor(db.Model):
    __tablename__ = 'sensor'
    id = db.Column(db.Integer,primary_key=True)
    device_id = db.Column(db.Integer,db.ForeignKey('device.id'))
    sensor_name = db.Column(db.String(20), nullable=False)
    data_type = db.Column(db.String(20), nullable=False)
    field_name = db.Column(db.String(20), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    decimal_digit = db.Column(db.Integer, nullable=False, default=0)
    max_value = db.Column(db.Float, nullable=False)
    min_value = db.Column(db.Float, nullable=False)
    icon = db.Column(db.String(100))
    sort_code = db.Column(db.Integer, default=0)
    sensor_type = db.Column(db.Integer, nullable=False, default=0)  # 0 采集数据 1 设备状态



class DeviceCmd(db.Model):
    __tablename__ = 'device_cmd'
    id = db.Column(db.Integer,primary_key=True)
    device_id = db.Column(db.Integer,db.ForeignKey('device.id'))
    dtu_id = db.Column(db.String(20))
    cmd_type = db.Column(db.Integer)
    cmd_txt = db.Column(db.String(100))
    cmd_date = db.Column(db.DateTime,default=datetime.now)

class DeviceLog(db.Model):
    __tablename__ = 'device_log'
    id = db.Column(db.Integer,primary_key=True)
    device_id = db.Column(db.Integer,db.ForeignKey('device.id'))
    log_type = db.Column(db.String(20))
    log_content = db.Column(db.String(200))
    log_date = db.Column(db.DateTime,default=datetime.now)