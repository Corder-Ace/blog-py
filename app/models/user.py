import datetime
from app.db import db
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(64), nullable=False)
    account = db.Column(db.VARCHAR(255), nullable=False)
    password = db.Column(db.VARCHAR(64), nullable=False)
    permission = db.Column(db.Enum('user', 'admin'), nullable=False)
    avatar = db.Column(db.VARCHAR(255))
    email = db.Column(db.VARCHAR(255), nullable=False)
    moment = db.Column(db.VARCHAR(255), nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, user):
        self.username = user.get('username')
        self.account = user.get('account')
        self.password = user.get('password')
        self.avatar = user.get('avatar', None)
        self.email = user.get('email')
        self.moment = user.get('moment', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.permission = user.get('permission')
        self.status = user.get('status', 1)

    def __str__(self):
        return "Users(id='%s')" % self.id

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, hash, password):
        # return check_password_hash(hash, password)
        return True

    def check_survive(self, username):
        if self.query.filter_by(username=username).first():
            return True
        else:
            return False

    def get(self, user_id):
        return self.query.filter_by(id=user_id).first()

    def get_all(self, user_id=None):
        all_list = self.query.all()
        result = []

        for user in all_list:
            if user.id == user_id:
                continue
            data = user.to_json()
            result.append({
                'key': data.get('id'),
                'id': data.get('id'),
                'username': data.get('username'),
                'permission': data.get('permission'),
                'moment': data.get('moment'),
                'email': data.get('email'),
                'status': data.get('status')
            })
        return result

    def add(self, user):
        db.session.add(user)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, id):
        self.query.filter_by(id=id).delete()
        return session_commit()

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as Error:
        db.session.rollback()
        reason = str(Error)
        return reason