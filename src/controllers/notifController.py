from flask import request, Blueprint, g, render_template
from ..models.UserModel import UserModel, UserSchema
from ..models.NotifModel import NotifModel
from src.jsonResponse import custom_response
from ..shared.Authentication import Auth
import json


notif_api = Blueprint('notif', __name__)
user_schema = UserSchema()



@notif_api.route('/delete_one_notif_by_notif_id/<string:notif_id>', methods=['GET'])
@Auth.auth_required
def delete_one_notif_by_notif_id(notif_id):
    notif_return = NotifModel.delete_one_notif_by_notif_id_and_user_id(g.user.get('id'), notif_id)
    if notif_return['nModified'] == 1:
        return custom_response({'success': 'Notif delete.'}, 200)
    return custom_response({'error': 'Notif not found.'}, 200)


@notif_api.route('/get_my_notif', methods=['GET'])
@Auth.auth_required
def get_my_notif():
    all_notif = list(NotifModel.get_all_notif_by_user_id(g.user.get('id')))[0]
    li_notif = {
        'id': str(all_notif['_id']),
        'user_id': all_notif['user_id'],
        'data': []
    }
    for notif in all_notif['data']:
        li_notif['data'].append({
            'id': str(notif['_id']),
            'notif': notif['notif']
        })
    return custom_response({'success': li_notif}, 200)


@notif_api.route('/delete_all_notif', methods=['GET'])
@Auth.auth_required
def delete_all_notif():
    NotifModel.delete_all_notif_by_id_user(g.user.get('id'))
    return custom_response({'success': 'Deleting all.'}, 200)


@notif_api.route('/all', methods=['GET'])
def allnotif():
    array = []
    test = NotifModel.get_all()
    for t in test:
        print(str(t))
        array.append(str(t))
    return custom_response({'success': array}, 200)


@notif_api.route('/delete', methods=['GET'])
def deletenotif():
    NotifModel.test()
    array = []
    test = NotifModel.get_all()
    for t in test:
        array.append(t['users'])
    return custom_response({'success': array}, 200)
