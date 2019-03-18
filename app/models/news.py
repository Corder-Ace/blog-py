import json
from app.db import db, session_commit
from app.auth.auths import get_user_info
import datetime


class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auth_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('Users', backref=db.backref('news'), uselist=False)
    title = db.Column(db.VARCHAR(255), nullable=False)
    desc = db.Column(db.VARCHAR(255), nullable=False)
    icon = db.Column(db.VARCHAR(255))
    content = db.Column(db.Text(65535), nullable=False)
    path = db.Column(db.Text(65535))
    publish_time = db.Column(db.VARCHAR(255), nullable=False)
    category = db.Column(db.Enum('origin', 'outside'), nullable=False)


    def __init__(self, news):
        self.title = news.get('title')
        self.desc = news.get('desc')
        self.auth_id = news.get('auth_id')
        self.icon = news.get('icon', ' ')
        self.content = news.get('content')
        self.path = news.get('paths')
        self.publish_time = news.get('publish_time', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.category = news.get('category')
        self.status = news.get('status', "1")

    def get_news(self):
        all_news = None
        result = []
        user_info = get_user_info()
        user_id = user_info.get('id')
        user_permission = user_info.get('permission')
        if user_permission != 'admin':
            all_news = self.query.filter_by(auth_id=user_id)
        else:
            all_news = self.get_all_news(self)

        if not len(all_news):
            return []
        for news in all_news:
            item = news.to_json()
            result.append({
                'id': item.get('id'),
                'title': item.get('title'),
                'desc': item.get('desc'),
                'category': item.get('category'),
                'publish_time': item.get('publish_time')
            })
        return result

    def get_all_news(self):
        result = []
        all_news_list = self.query.all()
        for news in all_news_list:
            item = news.to_json()
            result.append({
                'id': item.get('id'),
                'title': item.get('title'),
                'desc': item.get('desc'),
                'category': item.get('category'),
                'publish_time': item.get('publish_time')
            })
        return result

    def get_news_by_id(self, news_id):
        result = self.query.filter_by(id=news_id).first()
        return result


    def add(self, news):
        db.session.add(news)
        session_commit()

    def delete(self, news_id):
        self.query.filter_by(id=news_id).delete()
        return session_commit()

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


