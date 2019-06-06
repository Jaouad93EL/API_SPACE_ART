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


@user_api.route('/all_post/<int:id_user>', methods=['GET'])
@Auth.auth_required
def create_post(id_user):
    post_in_db = PostModel.get_post_all(id_user)
    if post_in_db:
        list_post = []
        [list_post.append(post_schema.dump(a).data) for a in post_in_db]
        return custom_response({'successful': list_post}, 200)
    return custom_response({'error': 'Post not exist.'}, 400)