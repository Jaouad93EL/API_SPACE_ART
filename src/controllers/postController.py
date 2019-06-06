from flask import request, Blueprint, g
from .mailController import login_success,randomString
from ..models.UserModel import UserModel
from ..models.PostModel import PostModel, PostSchema
from ..models.RevokedTokenModel import RevokedTokenModel
from src.jsonResponse import custom_response
from ..shared.Authentication import Auth
from ..Google_storage import google


user_api = Blueprint('users', __name__)
post_schema = PostSchema()

@user_api.route('/create_post', methods=['POST'])
def create():
    req_data = request.get_json()
    data, error = post_schema.load(req_data)