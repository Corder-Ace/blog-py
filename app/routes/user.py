import json
from flask import request, Blueprint
from app.db.user import get_all, search, create_user, toggle_user_status
users = Blueprint('users', __name__)


@users.route('/get_users', methods=['GET'])
def select_all_user():
    result = []
    for item in get_all():
        result.append({
            'id': item['id'],
            'username': item['username'],
            'email': item['email'],
            'permission': item['permission'],
            'status': item['status'],
            'avatar': item['avatar'],
            'moment': item['moment']
        })
    data = {
        'result': result,
        'status': 200
    }
    return json.dumps(data)


@users.route('/register', methods=['POST'])
def register_user():
    reg_info = request.get_json()
    user = search(reg_info.get('username', None))

    if user is None or user.username.strip() == '':
        try:
            create_user(reg_info)
        except Exception as Error:
            if Error:
                return json.dumps({
                    "status": 403,
                    "msg": '创建用户失败,请稍后再试!'
                })
        else:
            return json.dumps({
                "status": 200,
                "msg": '创建成功！'
            })
    else:
        return json.dumps({
            "status": 200,
            "msg": "用户已存在！"
        })


@users.route('/frozen_user/<user_id>', methods=['GET'])
def frozen_user(user_id):
    try:
        toggle_user_status(user_id)
    except Exception as Error:
        if Error:
            return json.dumps({
                'status': 403,
                'msg': '切换状态失败！'
            })
    return select_all_user()
