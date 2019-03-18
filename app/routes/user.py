from flask import request, Blueprint, jsonify
# from app.db import r
from app.models.user import Users
from app.auth.auths import authenticate, identify, get_user_info
from ..common import trueReturn, falseReturn, check_user
users = Blueprint('users', __name__)


# 登陆
@users.route('/login', methods=['POST'])
def login():
    login_info = request.get_json()
    if 'account' not in login_info:
        return jsonify(falseReturn({}, '用户名不能为空！'))

    if 'password' not in login_info:
        return jsonify(falseReturn({}, '密码不能为空！'))

    # authenticate 包含了密码验证
    account = login_info.get('account')
    password = login_info.get('password')
    return authenticate(account, password)


# 登出
@users.route('/logout', methods=['GET'])
def logout():
    user_id = get_user_info()
    # try:
    #     do something 这里应该清空redis和cookie
    # except Exception as e:
    #     if e:
    #         return jsonify(falseReturn({}, '登出失败,请稍后再试!'))
    return jsonify(trueReturn({}, '登出成功!'))


# 获取全部用户信息
@users.route('/get_users', methods=['GET'])
@identify
def select_all_user():
    try:
        user_info = get_user_info()
        result = Users.get_all(Users, user_info.get('permission'), user_info.get('id'))
    except Exception as Error:
        print(Error)
        return jsonify(falseReturn({}, '查询失败，请稍后再试！'))
    return jsonify(trueReturn(result, '获取成功!'))


# 添加用户
@users.route('/add', methods=['POST'])
@identify
def add_user():
    reg_info = request.get_json()
    # 数据验证
    check_info = check_user(reg_info)
    if not isinstance(check_info, bool):
        return check_info
    if not Users.check_survive(Users, reg_info.get('username')):
        try:
            user = Users(reg_info)
            Users.add(Users, user)
        except Exception as e:
            if e:
                return jsonify(falseReturn({}, '创建用户失败，请稍后再试!'))
        if user.id:
            user_info = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'permission': user.permission
            }
            return jsonify(trueReturn(user_info, '添加用户成功!'))
    return jsonify(falseReturn({}, '该用户已存在!'))


# 获取指定用户信息
@users.route('/get_user/<user_id>', methods=['GET'])
@identify
def get_user_by_id(user_id):
    user = Users.get(Users, user_id)
    if not user:
        return jsonify(falseReturn({}, '该用户不存在!'))
    result = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'permission': user.permission
    }
    return jsonify(trueReturn(result, '获取成功!'))


# 切换账号状态
@users.route('/frozen_user/<user_id>', methods=['GET'])
@identify
def frozen_user(user_id):
    try:
        user = Users.get(Users, user_id)
        user.status = not user.status
        Users.update(Users)
    except Exception as Error:
        if Error:
            return jsonify(falseReturn({}, '切换状态失败!'))
    return select_all_user()


# 更新用户信息
@users.route('/update_user', methods=['POST'])
@identify
def update_user():
    update_info = request.get_json()
    user = Users.get(Users, update_info.get('id'))
    if not user:
        return jsonify(falseReturn({}, '该用户不存在'))
    try:
        user.username = update_info.get('username', user.username)
        user.password = update_info.get('new_password', user.password)
        user.email = update_info.get('email', user.email)
        user.permission = update_info.get('permission', user.permission)
        Users.update(Users)
    except Exception as e:
        if e:
            return jsonify(falseReturn({}, '修改信息失败, 请稍后再试!'))
    return select_all_user()


# 删除指定用户
@users.route('/remove_user/<user_id>', methods=['GET'])
@identify
def remove_user(user_id):
    user = Users.get(Users, user_id)
    if not user:
        return jsonify(falseReturn({}, '该用户不存在!'))
    try:
        Users.delete(Users, user_id)
    except Exception as e:
        if e:
            return jsonify(falseReturn({}, '删除用户失败,请稍后再试!'))
    return select_all_user()
