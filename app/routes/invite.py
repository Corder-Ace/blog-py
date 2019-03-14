import json
from app.models.invite import Invite
from app.auth.auths import identify, get_user_id
from flask import request, Blueprint, jsonify
from ..common import trueReturn, falseReturn
invite = Blueprint('invite', __name__)


@invite.route('/get_all_invite', methods=['GET'])
def get_all_invite():
    return json.dumps({
        'status': 200
    })


@invite.route('/create_invite', methods=['POST'])
def create_invite():
    invite_info = request.get_json()
    invite_info['release_id'] = get_user_id()
    new_invite = Invite(invite_info)
    Invite.create_invite(Invite, new_invite)
    return jsonify(trueReturn({}, '创建成功！'))


@invite.route('/invites', methods=['GET'])
def get_invites():
    result = Invite.get_invites(Invite)

    return jsonify(trueReturn({}, '获取成功！'))