from app.db import db
import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(64), unique=True, nullable=False)
    account = db.Column(db.VARCHAR(64), unique=True, nullable=False)
    password = db.Column(db.VARCHAR(64), nullable=False)
    permission = db.Column(db.Enum('user', 'admin'), nullable=False)
    avatar = db.Column(db.VARCHAR(255))
    email = db.Column(db.VARCHAR(255), unique=True, nullable=False)
    moment = db.Column(db.VARCHAR(255), unique=True, nullable=False)
    status = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, user):
        self.username = user.get('username')
        self.account = user.get('account')
        self.password = user.get('password')
        self.avatar = user.get('avatar', None)
        self.email = user.get('email')
        self.moment = user.get('moment', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.permission = user.get('permission')
        self.status = user.get('status', 1)

    def __repr__(self):
        return '<User %r>' % self.username

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict