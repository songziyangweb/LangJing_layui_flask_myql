from app import db
from datetime import datetime

class SensorParam(db.Model):
    __tablename__ = "sensor_param"
    id = db.Column(db.Integer,primary_key=True)
    sensor_name = db.Column(db.String(20),nullable=False,unique=True)
    data_type = db.Column(db.String(20),nullable=False)
    field_name = db.Column(db.String(20),nullable=False,index=True,unique=True)
    unit = db.Column(db.String(20),nullable=False)
    decimal_digit = db.Column(db.Integer,nullable=False,default=0)
    max_value = db.Column(db.Float,nullable=False)
    min_value = db.Column(db.Float,nullable=False)
    icon = db.Column(db.String(100))
    sort_code = db.Column(db.Integer,default=0)
    sensor_type = db.Column(db.Integer,nullable=False,default=0,index=True) # 0 采集数据 1 设备状态

    checked = False
    def to_json(self):
        return {
            'id':self.id,
            'sensor_name':self.sensor_name,
            'data_type':self.data_type,
            'field_name':self.field_name,
            'unit':self.unit,
            'decimal_digit':self.decimal_digit,
            'max_value':self.max_value,
            'min_value':self.min_value,
            'icon':self.icon,
            'sort_code':self.sort_code,
            'sensor_type':self.sensor_type,
            'checked':self.checked
        }

class SensorParamData(db.Model):
    __tablename__ = 'sensor_param_data'
    id = db.Column(db.Integer,primary_key=True)
    sensor_param_id = db.Column(db.Integer,db.ForeignKey("sensor_param.id"))
    sensor_name = db.Column(db.String(20),nullable=False)
    sensor_field = db.Column(db.String(20),nullable=False,index=True)
    min_value = db.Column(db.Float)
    max_value = db.Column(db.Float)
    show_txt = db.Column(db.String(50))
    description = db.Column(db.String(100))

