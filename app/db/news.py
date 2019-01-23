from . import db
from app.models.news import News


# 创建用户
def create_news(news_info):
    news = News(news_info)
    db.session.add(news)
    db.session.commit()
