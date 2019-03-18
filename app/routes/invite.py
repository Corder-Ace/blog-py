from app.models.invite import Invite
from app.auth.auths import identify, get_user_info
from flask import request, Blueprint, jsonify
from ..common import trueReturn, falseReturn
invite = Blueprint('invite', __name__)


# 创建一个新的招聘
@invite.route('/create_invite', methods=['POST'])
@identify
def create_invite():
    invite_info = request.get_json()
    invite_info['release_id'] = get_user_info().get('id')
    new_invite = Invite(invite_info)
    Invite.create_invite(Invite, new_invite)
    return jsonify(trueReturn({}, '创建成功！'))


# 获取所有的招聘信息
@invite.route('/invites', methods=['GET'])
def get_invites():
    try:
        result = Invite.get_invites_all(Invite)
    except Exception as Error:
        # 这里可以考虑写日志
        print(Error)
        return jsonify(falseReturn({}, '获取失败，请稍后再试！'))

    return jsonify(trueReturn(result, '获取成功！'))
