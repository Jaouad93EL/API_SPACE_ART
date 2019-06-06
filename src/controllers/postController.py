from flask import request, Blueprint, g
from ..models.PostModel import PostModel, PostSchema
from src.jsonResponse import custom_response
from ..shared.Authentication import Auth


user_api = Blueprint('users', __name__)
post_schema = PostSchema()

@user_api.route('/create_post', methods=['POST'])
@Auth.auth_required
def create_post():
    req_data = request.get_json()
    data, error = post_schema.load(req_data)
    if error:
        return custom_response(error, 400)
    post = PostModel(data, g.user.get('id'))
    post.save()
    return custom_response({'success': 'Post created'}, 200)
