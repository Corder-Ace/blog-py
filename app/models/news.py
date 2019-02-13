from app.db import db, session_commit
import datetime


class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auth_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('Users', backref=db.backref('news'), uselist=False)
    title = db.Column(db.VARCHAR(255), unique=True, nullable=False)
    icon = db.Column(db.VARCHAR(255), nullable=False)
    content = db.Column(db.VARCHAR(255), nullable=False)
    publish_time = db.Column(db.VARCHAR(255), nullable=False)
    status = db.Column(db.Enum('0', '1', '2'), nullable=False)

    def __init__(self, news):
        self.title = news.get('title')
        self.auth_id = news.get('auth_id')
        self.icon = news.get('icon')
        self.content = news.get('content')
        self.publish_time = news.get('publish_time', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.status = news.get('status', "1")

    def get_news(self, user_id, permission):
        if permission:
            all_news = self.query.all()
        else:
            all_news = self.query.filter_by(auth_id=user_id)

        result = []
        for news in all_news:
            result.append(news.to_json())
        return result

    def add(self, news):
        db.session.add(news)
        session_commit()

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


