from app import db
from datetime import datetime
from flask_login import UserMixin,AnonymousUserMixin
from app import db,loginManager

@loginManager.user_loader
def load_user(user_id):
    return User.query.filter(User.id==user_id).first()

class User(db.Model,UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,index=True)
    realname = db.Column(db.String(80),default=' ')
    pwd = db.Column(db.String(100),nullable=False)
    create_date = db.Column(db.DATETIME,index=True,default=datetime.now)
    sex = db.Column(db.String(100))


    def __init__(self,username,realname,pwd,id,sex):
        self.id=id
        self.sex=sex
        self.username = username
        self.realname = realname
        self.pwd = pwd
    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
        return str(self.id)
    def to_json(self):
        return {
            'id':self.id,
            'username':self.username,
            'realname':self.realname,
            'pwd':self.pwd,
            'sex':self.sex,
            'create_date':self.create_date.strftime('%Y-%m-%d %H:%M:%S')
        }
