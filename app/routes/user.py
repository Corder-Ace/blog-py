import json
from flask import request, Blueprint
from app.models.user import Users
from app.db.user import toggle_user_status
from app.auth.auths import Auth, identify
users = Blueprint('users', __name__)


@users.route('/login', methods=['POST'])
def login():
    login_info = request.get_json()
    account = login_info.get('account')
    password = login_info.get('password')
    return Auth.authenticate(Auth, account, password)


@users.route('/get_users', methods=['GET'])
@identify
def select_all_user():
    result = Users.get_all(Users)
    data = {
        'result': result,
        'status': 200
    }
    return json.dumps(data)


@users.route('/add', methods=['POST'])
@identify
def add_user():
    reg_info = request.get_json()
    if not Users.check_survive(Users, reg_info.get('username')):
        try:
            user = Users(reg_info)
            Users.add(Users, user)
        except Exception as e:
            if e:
                return json.dumps({
                    'status': 403,
                    'msg': '创建用户失败，请稍后再试！'
                })
        if user.id:
            returnUser = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'permission': user.permission
            }
            return json.dumps({
                'result': returnUser,
                'status': 200
            })
    else:
        return json.dumps({
            'status': 200,
            'msg': '该用户已存在！'
        })


@users.route('/frozen_user/<user_id>', methods=['GET'])
@identify
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
