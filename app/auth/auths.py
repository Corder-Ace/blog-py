import jwt, datetime, time, re
from app.models.user import Users
from flask import jsonify, request
from functools import wraps
from .. import common


class Auth:
    @staticmethod
    def encode_auth_token(user_id, login_time, permission):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=15),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ace',
                'data': {
                    'id': user_id,
                    'login_time': login_time,
                    'permission': permission
                }
            }
            return jwt.encode(payload, 'ace', algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, 'ace', options={'verify_exp': False})
            date_now = int(time.time())
            if 'data' in payload and 'id' in payload['data'] and date_now < payload.get('exp'):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return 'Token无效'

    def authenticate(self, account, password):
        userinfo = Users.query.filter_by(account=account).first()
        login_time = int(time.time())
        if userinfo is None:
            return jsonify(common.falseReturn({}, '该用户不存在'))
        else:
            if Users.check_password(Users, userinfo.password, password):
                token = self.encode_auth_token(userinfo.id, login_time, userinfo.permission)
                return jsonify(common.trueReturn(token.decode(), '登陆成功！'))
            else:
                return jsonify(common.falseReturn({}, '账号或密码不正确'))


authorizedRoutes = [r'/api/v1/user/get_users', r'^(/api/v1/user/frozen_user/)+[\d]$']


def check_auth_path(permission, url):
    for reg in authorizedRoutes:
        if re.match(reg, url) and permission != 'admin':
            return False
    return True


def identify(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token_arr = auth_header.split(" ")
            if not auth_token_arr or auth_token_arr[0] != 'JWT' or len(auth_token_arr) != 2:
                result = common.tokenLoseReturn(' ', '请传递正确的验证信息')
            else:
                auth_token = auth_token_arr[1]
                payload = Auth.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user = Users.get(Users, payload['data']['id'])
                    if user is None:
                        result = common.falseReturn({}, '该用户不存在!')
                    elif not check_auth_path(payload['data']['permission'], request.path):
                        result = common.falseReturn({}, '无权限!')
                    else:
                        return func(*args, **kwargs)
                else:
                    result = common.falseReturn('', payload)
        else:
            result = common.falseReturn('', '没有提供认证token')
        return jsonify(result)
    return decorate





