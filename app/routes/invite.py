import json
from app.models.invite import Invite
from flask import request, Blueprint
invite = Blueprint('invite', __name__)

@invite.route('/get_all_invite', methods=['GET'])
def get_all_invite():
