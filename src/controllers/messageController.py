from flask import request, Blueprint, g, render_template
from ..models.UserModel import UserModel, UserSchema
from ..models.PrivateModel import PrivateModel
from src.jsonResponse import custom_response
from ..shared.Authentication import Auth
import json


message_api = Blueprint('message', __name__)
user_schema = UserSchema()

@message_api.route('/get_my_private_conversation/<int:test>', methods=['GET'])
def get_my_private_conversation(test):
    li_conv = []
    all_conv = PrivateModel.get_all_private_conversion_by_user_id([test])
    for conv in all_conv:
        li_conv.append({'id': str(conv['_id']),'users': conv['users'], 'last_message': conv['data'][0]})
    return custom_response({'success': li_conv}, 200)


@message_api.route('/leave_private_conversation/<int:test>/<string:id_conv>', methods=['GET'])
def leave_private_conversation(test, id_conv):
    PrivateModel.leave_private_conversation(test, id_conv)
    return custom_response({'success': id_conv}, 200)


@message_api.route('/get_one_conv/<string:id_conv>', methods=['GET'])
def get_one_conv(id_conv):
    PrivateModel.get_one_private_conversation_by_id_conv(id_conv)
    return custom_response({'success': id_conv}, 200)


@message_api.route('/delete', methods=['GET'])
def deleteallmessage():
    PrivateModel.test()
    array = []
    test = PrivateModel.get_all()
    for t in test:
        array.append(t['users'])
    return custom_response({'success': array}, 200)


@message_api.route('/all', methods=['GET'])
def allmessage():
    array = []
    test = PrivateModel.get_all()
    for t in test:
        print(str(t))
        array.append(str(t))
    return custom_response({'success': array}, 200)
