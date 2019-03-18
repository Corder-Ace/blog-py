import time, os, json
from app.models.news import News
from app.auth.auths import identify, get_user_info
from flask import request, Blueprint, jsonify
from ..common import trueReturn, falseReturn, check_user, remove_images
news = Blueprint('news', __name__)
root = '/home/moyun/static/images'


# 存储图片，返回存储路径
@news.route('/save_images', methods=['POST'])
def save_images():
    image_prefix = '{}_'.format(request.form.get('file_name'))
    files = request.files
    file_count = len(files)
    paths = []
    if not file_count:
        return jsonify(trueReturn({}, '存储失败，图片为空！'))
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


# 获取指定文章内容
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


# 获取所有文章
@news.route('/get_all_news', methods=['GET'])
def get_all_news():
    try:
        # 获取所有的新闻
        result = News.get_all_news(News)
        return jsonify(trueReturn(result, '获取成功！'))
    except Exception as Error:
        if Error:
            print(Error)
            return jsonify(falseReturn({}, '获取失败！'))


# 创建文章
@news.route('/create_news', methods=['POST'])
@identify
def create():
    form_data = request.form
    news_info = {
        "title": str(form_data.get('title')),
        "content": form_data.get('content'),
        "category": form_data.get('category'),
        "desc": form_data.get('desc'),
        "paths": form_data.get('paths')
    }
    # icon = request.files.get('icon')
    try:
        news_info['auth_id'] = get_user_info().get('id')
        new_news = News(news_info)
        News.add(News, new_news)
    except Exception as Error:
        if Error:
            print(Error)
            return jsonify(falseReturn({}, '创建失败！'))

    return jsonify(trueReturn({}, '创建成功！'))


# 删除文章
@news.route('/delete_news/<news_id>', methods=['DELETE'])
@identify
def delete_news_by_id(news_id):
    try:
        delete_news = News.get_news_by_id(News, news_id)
        if not delete_news:
            return jsonify(falseReturn({}, '该新闻不存在！'))
        paths = delete_news.path.split(',')
        if len(paths):
            for path in paths:
                os.remove('{}/{}'.format(root, path))
        News.delete(News, news_id)
    except Exception as Error:
        print(Error)
        return jsonify(falseReturn({}, '删除失败，请稍后再试！'))
    return jsonify(trueReturn({}, '删除成功！'))


# 更新文章
@news.route('/update', methods=['POST'])
@identify
def update_news_by_id():
    news_info = request.form
    update_news = News.get_news_by_id(News, news_info.get('news_id'))
    try:
        # 先把原来存储的图片删了
        remove_images(update_news.path)
        update_news.title = news_info.get('title', update_news.title)
        update_news.content = news_info.get('content', update_news.content)
        update_news.path = news_info.get('path', update_news.path)
        update_news.desc = news_info.get('desc', update_news.desc)
        News.update(News)
    except Exception as Error:
        print(Error)
        return jsonify(falseReturn({}, '更新失败'))
    return jsonify(trueReturn({}, '更新成功！'))
