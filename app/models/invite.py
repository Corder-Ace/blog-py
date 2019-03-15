from app.db import db, session_commit
import datetime


class Invite(db.Model):
    __tablename__ = 'invite'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    release_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    release = db.relationship('Users', backref=db.backref('invite'), uselist=False)
    title = db.Column(db.VARCHAR(255), nullable=False)
    count = db.Column(db.Integer(), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    publish_time = db.Column(db.VARCHAR(255), nullable=False)
    status = db.Column(db.Enum('0', '1', '2'), nullable=False)

    def __init__(self, invite):
        self.title = invite.get('title')
        self.release_id = invite.get('release_id', 1)
        self.content = invite.get('content')
        self.count = invite.get('count')
        self.publish_time = invite.get('publish_time', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.status = invite.get('status', "1")

    def get_invites(self, user_id, permission):
        result = []
        if permission:
            invites = self.query.all()
        else:
            invites = self.query.filter_by(release_id=user_id)

        for invite in invites:
            result.append(invite.to_json())
        return result

    def get_invites_all(self):
        invites = self.query.all()
        result = []
        for invite in invites:
            result.append(invite.to_json())
        return result


    def create_invite(self, invite):
        db.session.add(invite)
        session_commit()

    def delete(self, invite_id):
        self.query.filter_by(id=invite_id).delete()
        return session_commit()

    def update(self):
        return session_commit()

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict