import re
from flask import jsonify


def isEmail(email):
    str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    return re.match(str, email)


def trueReturn(data, msg):
    return {
        "status": 200,
        "result": data,
        "msg": msg
    }


def falseReturn(data, msg):
    return {
        "status": 403,
        "result": data,
        "msg": msg
    }


def tokenLoseReturn(data, msg):
    return {
        "status": 401,
        "result": data,
        "msg": msg
    }


def check_user(users):
    if 'username' not in users or not users.get('username').strip():
        return jsonify(falseReturn({}, '用户名不能为空!'))
    if 'password' not in users or not users.get('password').strip():
        return jsonify(falseReturn({}, '密码不能为空!'))
    if 'account' not in users or not users.get('account').strip():
        return jsonify(falseReturn({}, '账户不能为空!'))
    if 'email' not in users or not users.get('email').strip():
        return jsonify(falseReturn({}, '邮箱不能为空!'))
    if not isEmail(users.get('email')):
        return jsonify(falseReturn({}, '请输入正确的邮箱地址!'))
    if 'permission' not in users or not users.get('permission').strip():
        return jsonify(falseReturn({}, '请设置用户权限!'))
    return True
