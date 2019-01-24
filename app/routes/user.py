from flask import request, Blueprint, jsonify
from app.models.user import Users
from app.auth.auths import Auth, identify
from .. import common
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
    return jsonify(common.trueReturn(data, '获取成功!'))


@users.route('/add', methods=['POST'])
@identify
def add_user():
    reg_info = request.get_json()
    check_info = common.check_user(reg_info)
    if not isinstance(check_info, bool):
        return check_info
    if not Users.check_survive(Users, reg_info.get('username')):
        try:
            user = Users(reg_info)
            Users.add(Users, user)
        except Exception as e:
            if e:
                return jsonify(common.falseReturn({}, '创建用户失败，请稍后再试！!'))
        if user.id:
            user_info = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'permission': user.permission
            }
            return jsonify(common.trueReturn(user_info, '添加用户成功!'))
    return jsonify(common.falseReturn({}, '该用户已存在!'))


@users.route('/frozen_user/<user_id>', methods=['GET'])
@identify
def frozen_user(user_id):
    try:
        user = Users.get(Users, user_id)
        user.status = not user.status
        Users.update(Users)
    except Exception as Error:
        if Error:
            return jsonify(common.falseReturn({}, '切换状态失败!'))
    return select_all_user()
