import jwt, datetime, time, re
from app.models.user import Users
from flask import jsonify, request
from functools import wraps
from ..common import trueReturn, falseReturn, tokenLoseReturn


class Auth:
    @staticmethod
    def encode_auth_token(user_id, login_time, permission, status):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=15),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ace',
                'data': {
                    'id': user_id,
                    'login_time': login_time,
                    'permission': permission,
                    'status': status
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
        user_info = Users.query.filter_by(account=account).first()
        login_time = int(time.time())
        if not user_info:
            return jsonify(falseReturn({}, '该用户不存在'))
        elif not user_info.status:
            return jsonify(falseReturn({}, '该账户已被冻结，请联系管理员!'))
        else:
            if Users.check_password(Users, user_info.password, password):
                token = self.encode_auth_token(user_info.id, login_time, user_info.permission, user_info.status)
                return jsonify(trueReturn(token.decode(), '登陆成功！'))
            else:
                return jsonify(falseReturn({}, '账号或密码不正确'))


authorizedRoutes = [r'/api/v1/user/get_users', r'^(/api/v1/user/frozen_user/)+[\d]$']


def check_auth_path(permission, url, status):
    if not status:
        return False
    for reg in authorizedRoutes:
        if re.match(reg, url) and permission != 'admin':
            return False
    return True


def identify(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token:
            auth_token_arr = access_token.split(" ")
            if not auth_token_arr or auth_token_arr[0] != 'JWT' or len(auth_token_arr) != 2:
                result = tokenLoseReturn(' ', '请传递正确的验证信息')
            else:
                auth_token = auth_token_arr[1]
                payload = Auth.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user = Users.get(Users, payload['data']['id'])
                    if user is None:
                        result = falseReturn({}, '该用户不存在!')
                    elif not check_auth_path(payload['data']['permission'], request.path, payload['data']['status']):
                        result = falseReturn({}, '无权限!')
                    else:
                        return func(*args, **kwargs)
                else:
                    result = falseReturn('', payload)
        else:
            result = falseReturn('', '没有提供认证token')
        return jsonify(result)
    return decorate





