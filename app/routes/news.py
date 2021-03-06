import json
from flask import request, Blueprint
from app.db.news import create_news
news = Blueprint('news', __name__)


@news.route('/get_all_news', methods=['GET'])
def get_all_news():
    return json.dumps({
        'status': 200
    })


@news.route('/create_news', methods=['POST'])
def create():
    news_info = request.get_json()
    try:
        create_news(news_info)
    except Exception as Error:
        if Error:
            print(Error)
            return json.dumps({
                'status': 403,
                'msg': '创建失败'
            })

    return json.dumps({
        'status': 200
    })


