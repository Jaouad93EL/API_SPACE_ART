from flask import request, Blueprint, g, render_template
from ..models.UserModel import UserModel, UserSchema
from src.jsonResponse import custom_response
from ..shared.Authentication import Auth
import json


search_api = Blueprint('search', __name__)
user_schema = UserSchema()

@search_api.route('/test', methods=['GET'])
def test():
    return custom_response({'success': 'test.'}, 200)
