import time, os, json
from app.models.news import News
from app.auth.auths import identify, get_user_id
from flask import request, Blueprint, jsonify
from ..common import trueReturn, falseReturn, check_user
news = Blueprint('news', __name__)
root = '/home/moyun/static/images'


@news.route('/save_images', methods=['POST'])
def save_images():
    image_prefix = '{}_'.format(request.form.get('file_name'))
    files = request.files
    file_count = len(files)
    paths = []
    if not file_count:
        # time.sleep(2)
        return jsonify(trueReturn({}, '存储失败，图片为空'))
    for index in range(file_count):
        image_name = '{}{}'.format(image_prefix, index)
        image = files.get(image_name)
        image_type = image.mimetype.split('/')[1]
        blob = image.read()
        create_time = time.time()
        path_name = '{}/{}.{}'.format(root, create_time, image_type)
        paths.append('{}.{}'.format(create_time, image_type))
        with open(path_name, 'wb') as image:
            image.write(blob)
    return jsonify(trueReturn(paths, '存储成功'))


@news.route('/get_news/<news_id>', methods=['GET'])
def get_news(news_id):
    result = News.get_news_by_id(News, news_id)
    author = result.author
    data = {
        "id": result.id,
        "author": author.username,
        "title": result.title,
        "content": str(result.content),
        "publish_time": result.publish_time,
        "category": result.category
    }
    return jsonify(trueReturn(data, '获取成功！'))


@news.route('/get_all_news', methods=['GET'])
def get_all_news():
    try:
        result = News.get_news(News)
        return jsonify(trueReturn(result, '获取成功！'))
    except Exception as Error:
        if Error:
            print(Error)
            return jsonify(falseReturn({}, '获取失败'))


@news.route('/create_news', methods=['POST'])
@identify
def create():
    form_data = request.form
    news_info = {
        "title": str(form_data.get('title')),
        "content": form_data.get('content'),
        "category": form_data.get('category'),
        "desc": form_data.get('desc')
    }
    # icon = request.files.get('icon')
    try:
        news_info['auth_id'] = get_user_id()
        new_news = News(news_info)
        News.add(News, new_news)
    except Exception as Error:
        if Error:
            print(Error)
            return jsonify(falseReturn({}, '创建失败！'))

    return jsonify(trueReturn({}, '创建成功！'))


