import json
from flask import request, Blueprint
from app.db.user import get_all, search, create_user
users = Blueprint('users', __name__)


@users.route('/', methods=['GET'])
def select_all_user():
    result = get_all()
    return json.dumps(result)


@users.route('/register', methods=['POST'])
def register_user():
    reg_info = request.get_json()
    user = search(reg_info.get('username', None))

    if user is None or user.username.strip() == '':
        try:
            create_user(reg_info)
        except Exception as Error:
            if Error:
                raise TypeError("创建用户失败：") from Error
            return json.dumps({
                "status": 403,
                "msg": '创建用户失败,请稍后再试!'
            })
        else:
            return json.dumps({
                "status": 200,
                "msg": '用户不存在'
            })
    else:
        return json.dumps({
            "status": 200,
            "msg": "用户已存在"
        })
