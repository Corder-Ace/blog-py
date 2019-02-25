import time, os
from app.models.news import News
from app.auth.auths import identify, get_user_id
from flask import request, Blueprint, jsonify
from ..common import trueReturn, falseReturn, check_user
news = Blueprint('news', __name__)
root = '/Users/ace/Desktop/blog-py/app/images'


@news.route('/save_images', methods=['POST'])
def save_images():
    image_prefix = '{}_'.format(request.form.get('file_name'))
    files = request.files
    file_count = len(files)
    paths = []
    if not file_count:
        return jsonify(falseReturn({}, '存储失败，图片为空'))
    for index in range(file_count):
        image_name = '{}{}'.format(image_prefix, index)
        blob = files.get(image_name).read()
        path_name = '{}/{}_{}.png'.format(root, image_name, time.time())
        paths.append(path_name)
        with open(path_name, 'wb') as image:
            image.write(blob)
    return jsonify(trueReturn(paths, '存储成功'))


@news.route('/get_news/<news_id>', methods=['GET'])
def get_news(news_id):
    result = News.get_news_by_id(News, news_id)
    return jsonify(trueReturn(result.to_json(), '获取成功！'))

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
def create():
    print(request.form.get('category'))
    print(len(request.files))
    file = request.files.get('images_0').read()
    with open('/Users/ace/Desktop/blog-py/app/images/images_0.png', 'wb') as image:
        image.write(file)
    news_info = request.get_json()

    try:
        news_info['auth_id'] = get_user_id()
        new_news = News(news_info)
        News.add(News, new_news)
    except Exception as Error:
        if Error:
            print(Error)
            return jsonify(falseReturn({}, '创建失败！'))

    return jsonify(trueReturn({}, '创建成功！'))


