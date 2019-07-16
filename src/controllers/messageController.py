from flask import request, Blueprint, g, render_template
from ..models.UserModel import UserModel, UserSchema
from src.jsonResponse import custom_response
from ..shared.Authentication import Auth


message_api = Blueprint('message', __name__)
user_schema = UserSchema()

@message_api.route('/private_message/<int:user_id>', methods=['GET'])
@Auth.auth_required
def message_private(user_id):
    ok = UserModel.private_conv()
    test = []
    for o in ok:
        test.append({'id': o['id']})
    return custom_response(test, 200)


@message_api.route('/test', methods=['GET'])
def test():
    return render_template('test.html')
